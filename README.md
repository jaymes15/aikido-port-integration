# Aikido Integration for Port Ocean

This integration syncs Aikido resources into [Port Ocean](https://www.getport.io/), enabling visibility and governance across your software catalog.

---

## 🚀 Getting Started

### ✅ Prerequisites

* Python `3.12.11` or later
* [Poetry](https://python-poetry.org/)
* [Port Ocean CLI](https://pypi.org/project/port-ocean/)
* [Helm](https://helm.sh/) (for local Kubernetes deployments)
* [Minikube](https://minikube.sigs.k8s.io/) (optional for local k8s)

---

### 🔧 Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone <repo-url>
   cd aikido
   ```

2. **Configure Environment Variables**

   ```sh
   cp env.example .env
   # Then edit .env and update credentials as needed
   ```

   **Required Environment Variables:**
   - `OCEAN__INTEGRATION__CONFIG__AIKIDO_CLIENT_ID` - Your Aikido client ID
   - `OCEAN__INTEGRATION__CONFIG__AIKIDO_CLIENT_SECRET` - Your Aikido client secret
   - `OCEAN__BASE_URL` - Your integration's public URL (for webhooks)

   **Example .env file:**
   ```bash
   OCEAN__BASE_URL=http://localhost:8000
   OCEAN__INTEGRATION__CONFIG__AIKIDO_CLIENT_ID=your_aikido_client_id
   OCEAN__INTEGRATION__CONFIG__AIKIDO_CLIENT_SECRET=your_aikido_client_secret
   OCEAN__INTEGRATION__CONFIG__AIKIDO_BASE_URL=https://app.aikido.dev/api/public/v1
   ```

3. **Configure Webhook Base URL**

   **Important**: Set the `OCEAN__BASE_URL` environment variable to your integration's public URL. This is crucial for webhook functionality as it determines the base URL for webhook endpoints.

   ```sh
   export OCEAN__BASE_URL="https://your-integration-domain.com"
   ```

   For local development, you can use:
   ```sh
   export OCEAN__BASE_URL="http://localhost:8000"
   ```

   > **Note**: The webhook endpoints will be available at `{OCEAN__BASE_URL}/webhook/`. This URL must be publicly accessible for Aikido to send webhook events.

4. **Create and Activate Virtual Environment**

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Install Port Ocean CLI**

   ```sh
   pip install "port-ocean[cli]"
   ```

6. **Install Dependencies (including dev)**

   ```sh
   poetry install
   ```

7. **Run the Integration**

   ```sh
   make run
   ```

---

## 📦 Features

* Syncs various Aikido resources into Port Ocean:

  * Issues
  * Issues Count

* Fully extendable and ready for production use.
* Designed for easy local and cloud deployment.

---

## 💪 Integration in Action

The integration syncs Aikido resources to Port Ocean and reflects them as green (healthy) exporters in the Port UI.

![Aikido Exporters Synced](aikido/docs/port-exporters-synced.png)

---

## 🧪 Local Deployment with Helm (Minikube)

Deploy Port Ocean locally using Helm and Minikube:

```sh
helm upgrade --install git-init port-labs/port-ocean \
  --set port.clientId=<PortClientId> \
  --set port.clientSecret=<PortClientSecret> \
  --set initializePortResources=true \
  --set integration.identifier=<Identifier> \
  --set integration.type="aikido" \
  --set integration.eventListener.type="POLLING" \
  --set integration.config.clientId=<aikidoClientId> \
  --set integration.config.clientSecret=<aikidoClientSecret>
```

> **Note:** Replace placeholder values (`<...>`) with your actual credentials.

---

## 🧰 Running Tests

Run all unit and integration tests with:

```sh
poetry run pytest
```

Useful options:

* Verbose mode: `pytest -v`
* Run matching pattern: `pytest -k <pattern>`

Tests are located in `aikido/tests/`, and new tests should follow the `test_*.py` naming convention.

---

## 📁 Project Structure

```
aikido/
├── auth/                # OAuth2 and token management
├── exporters/           # Exporters for each Aikido resource
├── http/                # HTTP client with retries
├── kind/                # Enum definitions for resource kinds
├── resync_handlers/     # Handlers for Port Ocean resync events
├── tests/               # Unit and integration tests
├── main.py              # Entrypoint: startup, loop, handler registration
.port/
├── resources/
│   ├── blueprints.json         # Blueprint schemas
│   └── port-app-config.yml     # Resource mapping config
├── spec.yaml                   # Integration metadata
Dockerfile                      # Container instructions
logging_config.py               # Centralized Loguru config
requirements.txt                # Python dependencies
README.md                       # Project documentation
```

---

## 📚 Resources

* [Port Integration Docs](https://docs.port.io/build-your-software-catalog/sync-data-to-catalog/)
* [Port Ocean SDK Docs](https://ocean.getport.io/develop-an-integration/)
* *(Replace with project-specific documentation if available)*

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open issues, suggest improvements, or submit pull requests.

---

## 📧 Support

For questions or help, please:

* Open an issue in the repository
* Contact the maintainers directly
