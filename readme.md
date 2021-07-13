# Azure Locust

Run distributed [Locust](https://locust.io/) load tests on _Azure Container Instances_. It's quick, cheap and scalable! Using 20 slaves you can achieve ~12 000 req/s!

![Locust Diagram](docs/locust-diagram.png)

You can deploy and manage resources using either: 
* [Azure Portal](https://portal.azure.com) - easier
* [Azure Cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) - faster 

## Azure Portal
Make sure you are logged in to [Azure Portal](https://portal.azure.com).

### 1. Deployment (Portal)

Click magick button (you can open it in new tab):

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FORBA%2Fazure-locust%2Fmaster%2FmainTemplate.json)

Then fill form with given values.

- **Subscription:** choose your subscription
- **Resource Group:** select existing Resource Group or create new one
- **Location:** North Europe (any allowed, but keep in mind its part of Locust DNS address!)
- **Instances (optional):**  number of slaves (one slave ~600rps)

![Custom Deployment](docs/custom-deployment.png)

Click **Purchase** and wait for deployment ends. Follow notifications on Azure Portal:

![Notification](docs/locust-notification.png)

Click **Go to resource group** to verify your deployment:

![Resource Group](docs/locust-rg.png)

Go to `xxxxxxxxxxxxx-master` and find out Locust FQDN - copy it.

![Locust Master](docs/locust-master.png)

### 2. Go to dashboard (Portal)

When deployment succeeded, your load generator is ready. Go to the above FQDN and port 8089: 

`http://xxxxxxxxxxxxx-master.northeurope.azurecontainer.io:8089` 

At this point you can start tests. 

![Locust Ready](docs/locust-ready.png)


### 3. Updating script (Portal)

Go to your Resource Group and click **Storage Account** named `xxxxxxxxxxxxx`. 

![Edit Storage](docs/locust-sa.png)

Click _File shares_ (scroll panel down).
Go to share called `scripts` and edit `locustfile.py` (click `...` and edit).
Edit contents of your new file and click _Save_.

![Edit Storage](docs/locust-save.png)

Then restart all containers called like *master* and *slave*.

![Acis](docs/locust-acis.png)

Click on each container to restart it:

![Reset](docs/locust-restart.png)

**Tip:** This step is really faster using Azure CLI.

### 4. Cleanup (Portal)

Go to your Resource Group and remove it (it will destroy all resources inside group). 
You will need to type Resource Group name to confirm.

![Remove](docs/locust-rm.png)

## Azure CLI

Login and set subscription context

```
az login
az account set --subscription <SubscriptionId>
```

### 1. Deployment (CLI)

**Step 1:** Setup your names
```
export RG=<ResourceGroup>
```

**Step 2:** Create Resource Group (if not exists)
```
az group create --name ${RG} --location northeurope
```

**Step 3:** Deploy ARM template
```
az group deployment create --resource-group ${RG} --query properties.outputs --template-file mainTemplate.json 
```
- To change number of instances append `--parameters instances=<n>`

**Step 4:** Note values of `prefix` and `url` from console output.

```json
{
  "outputs": {
    "prefix": {
      "type": "String",
      "value": "xxxxxxxxxxxxx"
    },
    "url": {
      "type": "String",
      "value": "http://xxxxxxxxxxxxx-master.northeurope.azurecontainer.io:8089"
    }
  }
}
```

### 2. Go to dashboard (CLI)

When deployment succeeded, your load generator is ready. Go to above `url` address. 

At this point you can start tests. 

### 3. Update script (CLI)

Upload your custom script. Replace account name with above `prefix`. You can change `--source` param if you want use different .py file:
```
az storage file upload --account-name <prefix> -s scripts --source locustfile.py --path locustfile.py
```
Then restart containers:
```
az container list --resource-group ${RG} --query '[].name' -o tsv | xargs -I {} az container restart --no-wait --resource-group ${RG} --name {} 
```

### 4. Cleanup (CLI)

Remove resources from Azure:
```
az group delete --name ${RG} --yes
```

## Disclaimer

* Load test affects target service performance. Never run load tests without service owner permission!
* Some services can block traffic from generator - you should whitelist Azure Region IPs ([Download prefixes](https://www.microsoft.com/download/details.aspx?id=56519)).
* After load tests cleanup Azure resources. You will be billed for running Azure Contianers Instance and Storage Account usage. You can check cost of ACI [here](https://azure.microsoft.com/en-us/pricing/details/container-instances/).