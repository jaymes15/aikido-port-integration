# Aikido Integration

This integration imports Aikido resources into Port.

## 📦 Features

- Syncs Aikido resources (issues, groups, cloud providers, code repositories, container images, and more) into Port Ocean.
- Designed for easy deployment and extension.

## ✅ Integration in Action

Below is a screenshot of the Aikido integration successfully syncing all resource types into Port Ocean:

![Aikido Exporters Synced](aikido/docs/port-exporters-synced.png)

- All exporters show a green status, indicating successful sync.
- The catalog was last updated recently, confirming recent activity.

## 🚀 Local Deployment to Minikube (Helm Reference)

> **Note:** The following command is for local deployment of Port Ocean to a minikube cluster using Helm.

```sh
helm upgrade --install git-init port-labs/port-ocean \
  --set port.clientId=<PortClientId> \
  --set port.clientSecret=<PortClientSecret> \
  --set initializePortResources=true \
  --set integration.identifier=<Identifier> \
  --set integration.type="github" \
  --set integration.eventListener.type="POLLING" \
  --set integration.config.aikidoClientId=<aikidoClientId> \
  --set integration.config.aikidoClientSecret=<aikidoClientSecret>
```

- Make sure your minikube cluster is running and Helm is installed.
- **Replace secrets and tokens with your own values as needed.**

---

## 🛠️ Development

- [Integration documentation](https://docs.port.io/build-your-software-catalog/sync-data-to-catalog/)  
  *(Replace this link with a link to this integration's documentation if available)*
- [Ocean integration development documentation](https://ocean.getport.io/develop-an-integration/)

---

## 📄 Project Structure

- `aikido/` – Main integration package
  - `aikido/exporters/` – Exporter classes for each Aikido resource (issues, groups, cloud providers, etc.)
  - `aikido/auth/` – Authentication logic (OAuth2, token refresh, etc.)
  - `aikido/http/` – HTTP client and retry logic
  - `aikido/kind/` – Enum definitions for resource kinds
  - `aikido/resync_handlers/` – Handlers for Port Ocean resync events, one per resource type
  - `aikido/main.py` – Entrypoint for the integration (startup, event loop, handler registration)
  - `aikido/tests/` – Unit and integration tests for the exporters and handlers
- `.port/` – Port Ocean configuration and blueprints
  - `resources/blueprints.json` – Blueprint schemas for all Aikido resource types
  - `resources/port-app-config.yml` – Mapping config for syncing Aikido data to Port
  - `spec.yaml` – Integration metadata for Port
- `logging_config.py` – Centralized logging setup using Loguru (console and file logging)
- `README.md` – Project documentation, setup, and usage instructions
- `requirements.txt` – Python dependencies for the integration
- `Dockerfile` – Container build instructions for deployment

> This structure makes it easy to extend the integration, add new resource types, or update configuration and blueprints as Aikido or Port evolve.

---

## 🤝 Contributing

Pull requests and issues are welcome!

---

## 📧 Support

For help, open an issue or contact the maintainers. 