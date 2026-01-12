# Ejercicio: Catálogo -> Dataset -> Contrato (EDC en el espacio de datos)

A continuación tienes los pasos básicos para que un conector que quiere consumir datos interactúe con un conector que los provee dentro del espacio de datos.
Los ejemplos están adaptados al entorno **appdev.agora-datalab.eu** y al conector **connector2**.

## **Paso 1: Consultar el catálogo del proveedor**

En este paso, el *consumidor* consulta el catálogo completo del *proveedor* para ver todos los datasets disponibles.
Para este ejemplo usamos `connector1` como *provider* y `connector2` como *consumer*.

```bash
curl --location 'http://connector2-connector:19193/management/v3/catalog/request' \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: connector2' \
  --data-raw '{
    "@context": { "@vocab": "https://w3id.org/edc/v0.0.1/ns/" },
    "@type": "CatalogRequest",
    "counterPartyAddress": "https://connector1.appdev.agora-datalab.eu/protocol",
    "counterPartyId": "connector1",
    "protocol": "dataspace-protocol-http"
  }' | jq .
```

### **Estructura general de una request EDC**

- **POST** -> Método HTTP que usamos para enviar la petición.  
- **URL de management** -> `.../management/v3/...` es la API interna del conector.  
- **Cabeceras**  
  - `Content-Type: application/json`  
  - `X-Api-Key: connector2`  
- **`@context`** -> Contexto JSON-LD.  
- **`@type`** -> Tipo de request (`CatalogRequest`, `DatasetRequest`, etc.).  
- **`counterPartyAddress`** -> URL pública del *provider* (`/protocol`).  
- **`counterPartyId`** -> ID lógico del conector remoto.  
- **`protocol`** -> Protocolo del dataspace: `"dataspace-protocol-http"`.



## **Catálogo federado (Federated Catalog)**

También puedes consultar un catálogo federado, que agrega datasets de múltiples proveedores.

```bash
curl --location 'http://connector2-connector:19193/management/v3/catalog/request' \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: connector2' \
  --data-raw '{
    "@context": { "@vocab": "https://w3id.org/edc/v0.0.1/ns/" },
    "@type": "CatalogRequest",
    "counterPartyAddress": "https://master-fc.appdev.agora-datalab.eu/catalog/v1alpha/catalog/query?",
    "counterPartyId": "master-fc",
    "protocol": "dataspace-protocol-http"
  }' | jq .
```

Aquí `master-fc` es el Federated Catalog del espacio de datos.



## **Paso 2: Ver información de un dataset concreto**

En este paso el *consumer* pide información detallada sobre un dataset específico antes de negociar un contrato.

Ejemplo de dataset: `iris-asset-con11.0.0` del catálogo de `connector1`.

```bash
curl --location 'http://connector2-connector:19193/management/v3/catalog/dataset/request' \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: connector2' \
  --data '{
    "@context": { "@vocab": "https://w3id.org/edc/v0.0.1/ns/" },
    "@type": "DatasetRequest",
    "@id": "iris-asset-con11.0.0",
    "counterPartyAddress": "https://connector1.appdev.agora-datalab.eu/protocol",
    "counterPartyId": "connector1",
    "protocol": "dataspace-protocol-http"
  }' | jq .
```

Puntos clave:

- `@type: "DatasetRequest"` -> pide información de **un único dataset**.  
- `@id` -> ID del dataset en el catálogo del provider.  
- El resto de campos sigue el mismo patrón del `CatalogRequest`.



## **Paso 3: Iniciar una negociación de contrato**

Ahora el *consumidor* inicia una negociación para poder acceder al dataset. 

```bash
curl --location 'http://connector2-connector:19193/management/v3/contractnegotiations' \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: connector2' \
  --data '{
    "@context": ["https://w3id.org/edc/connector/management/v0.0.1"],
    "@type": "ContractRequest",
    "counterPartyAddress": "https://connector1.appdev.agora-datalab.eu/protocol",
    "counterPartyId": "connector1",
    "protocol": "dataspace-protocol-http",
    "policy": {
      "@type": "Offer",
      "@id": "b2ZmZXItaXJpcy1jb24x:aXJpcy1hc3NldC1jb24xMS4wLjA=:ZTQwNjdmYzktODVjZC00YWFmLWIwZDctYTU0MjcxODk1Mjdk",
      "assigner": "connector1",
      "permission": [],
      "prohibition": [],
      "obligation": [],
      "target": "iris-asset-con11.0.0"
    },
    "callbackAddresses": []
  }' | jq .
```

### **Desglose de la política**

- `@type: "Offer"` -> Estamos proponiendo una oferta de contrato.  
- `assigner: "connector1"` -> Quien concede el derecho de uso (el provider).  
- `target` -> El dataset al que aplica el contrato.  
- `permission`, `prohibition`, `obligation` -> Listas vacías -> contrato sin restricciones adicionales.


## **Paso 4: Obtener el estado de la negociación**

Después de iniciar la negociación de contrato, puedes consultar su estado.  
Esto es útil para comprobar si el *provider* ha aceptado o rechazado la oferta.  
Si la oferta coincide con las condiciones definidas por el *provider*, la negociación debería progresar hasta el estado **FINALIZED**, generando un `contractAgreementId`.

Para consultar el estado, utiliza:

```bash
curl --location 'http://connector2-connector:19193/management/v3/contractnegotiations/c86f04f8-d928-4d6c-9c6e-f278be84b84a' \
  --header 'X-Api-Key: connector2' | jq .
```

Espera hasta que en la respuesta aparezca un campo:

- `"state": "FINALIZED"`
- `"contractAgreementId": "<ALGÚN_ID>"`

Ese `contractAgreementId` es necesario para iniciar la transferencia en el siguiente paso.

### Paso 5: Iniciar la transferencia de datos

Una vez que la negociación ha sido aceptada y tienes un contrato, puedes iniciar la transferencia de datos.

En este paso, el *consumer* solicita al *provider* que inicie la transferencia.  

!!! note
    Recuerda que los conectores no almacenan los datos, sino que los transfieren.  
    Hasta ahora, se ha usado el **plano de control** (catalog, dataset, contractnegotiations), pero la transferencia de datos se realiza a través del **plano de datos**.  
    En este caso, estamos utilizando `HttpData-PUSH`, donde el *consumer* expone un endpoint HTTP para que el *provider* envíe los datos.

Para iniciar la transferencia:

```bash
curl --location 'http://connector2-connector:19193/management/v3/transferprocesses' \
  --header 'Content-Type: application/json' \
  --header 'X-Api-Key: connector2' \
  --data '{
    "@context": ["https://w3id.org/edc/connector/management/v0.0.1"],
    "counterPartyAddress": "https://connector1.appdev.agora-datalab.eu/protocol",
    "connectorId": "connector1",
    "contractId": "ac7c232c-b20f-47f3-ad30-9e2635474151",
    "protocol": "dataspace-protocol-http",
    "transferType": "HttpData-PUSH",
    "dataDestination": {
      "type": "HttpData",
      "baseUrl": "https://webhook.site/b6c2cd57-de40-4e84-9aa3-3949d49d2e93",
      "path": "/",
      "method": "POST"
    }
  }' | jq .
```

- Sustituye `<CONTRACT_AGREEMENT_ID>` por el valor devuelto en el **Paso 4**.
- Esta operación devolverá un `@id`, que es el **ID de proceso de transferencia** (`transferProcessId`).

Guarda ese `@id`: lo vas a necesitar para obtener el `dataAddress` en el siguiente paso.

Puedes ver el estado del proceso de transferencia con:

```bash
curl --location 'http://connector2-connector:19193/management/v3/transferprocesses/97f75280-87c9-440f-8f92-7bb2cc021f93' \
  --header 'X-Api-Key: connector2' | jq .
```

