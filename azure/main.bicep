// Azure Bicep Template for The Hunter - Complete Infrastructure
// Deploys: Container Registry, PostgreSQL, Container Instances

param location string = 'eastus'
param environment string = 'staging'
param projectName string = 'the-hunter'

// Resource naming
var resourceGroupName = '${projectName}-${environment}'
var registryName = '${projectName}registry'
var dbServerName = '${projectName}-db-${environment}'
var dbName = 'the_hunter'
var apiContainerName = '${projectName}-api-${environment}'
var frontendContainerName = '${projectName}-frontend-${environment}'

// Database admin credentials (CHANGE THESE!)
param dbAdminUsername string = 'hunter'
@secure()
param dbAdminPassword string
@secure()
param secretKey string

// Tags for all resources
var tags = {
  project: projectName
  environment: environment
  managedBy: 'bicep'
  createdDate: utcNow('u')
}

// ============================================================================
// 1. Container Registry
// ============================================================================
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: registryName
  location: location
  tags: tags
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
  }
}

// Get registry credentials
output registryLoginServer string = containerRegistry.properties.loginServer
output registryUsername string = containerRegistry.listCredentials().username
@secure()
output registryPassword string = containerRegistry.listCredentials().passwords[0].value

// ============================================================================
// 2. PostgreSQL Database
// ============================================================================
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-12-01-preview' = {
  name: dbServerName
  location: location
  tags: tags
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    administratorLogin: dbAdminUsername
    administratorLoginPassword: dbAdminPassword
    version: '15'
    storage: {
      storageSizeGB: 32
    }
    backup: {
      backupRetentionDays: 7
      geoRedundantBackup: 'Disabled'
    }
    network: {
      delegatedSubnetResourceId: ''
      privateDnsZoneArmResourceId: ''
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

// Allow all Azure IPs
resource postgresFirewallRule 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-12-01-preview' = {
  parent: postgresServer
  name: 'AllowAllAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '255.255.255.255'
  }
}

// Database
resource database 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-12-01-preview' = {
  parent: postgresServer
  name: dbName
  properties: {
    charset: 'UTF8'
    collation: 'en_US.utf8'
  }
}

// Output connection string
output databaseHost string = postgresServer.properties.fullyQualifiedDomainName
output databaseConnectionString string = 'postgresql://${dbAdminUsername}:${dbAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}/${dbName}'

// ============================================================================
// 3. Container Instance - Backend API
// ============================================================================
resource apiContainer 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = {
  name: apiContainerName
  location: location
  tags: tags
  properties: {
    containers: [
      {
        name: apiContainerName
        properties: {
          image: '${containerRegistry.properties.loginServer}/the-hunter-api:latest'
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 1
            }
          }
          ports: [
            {
              port: 8000
              protocol: 'TCP'
            }
          ]
          environmentVariables: [
            {
              name: 'DATABASE_URL'
              secureValue: 'postgresql://${dbAdminUsername}:${dbAdminPassword}@${postgresServer.properties.fullyQualifiedDomainName}/${dbName}'
            }
            {
              name: 'SECRET_KEY'
              secureValue: secretKey
            }
            {
              name: 'DEBUG'
              value: 'false'
            }
            {
              name: 'LOG_LEVEL'
              value: 'info'
            }
            {
              name: 'ALLOWED_ORIGINS'
              value: 'http://localhost:4200,http://localhost:3000,https://${frontendContainerName}.${location}.azurecontainers.io'
            }
          ]
        }
      }
    ]
    osType: 'Linux'
    restartPolicy: 'Always'
    ipAddress: {
      type: 'Public'
      dnsNameLabel: apiContainerName
      ports: [
        {
          port: 8000
          protocol: 'TCP'
        }
      ]
    }
    imageRegistryCredentials: [
      {
        server: containerRegistry.properties.loginServer
        username: containerRegistry.listCredentials().username
        password: containerRegistry.listCredentials().passwords[0].value
      }
    ]
  }
}

output apiUrl string = 'http://${apiContainer.properties.ipAddress.fqdn}:8000'

// ============================================================================
// 4. Container Instance - Frontend
// ============================================================================
resource frontendContainer 'Microsoft.ContainerInstance/containerGroups@2023-05-01' = {
  name: frontendContainerName
  location: location
  tags: tags
  properties: {
    containers: [
      {
        name: frontendContainerName
        properties: {
          image: '${containerRegistry.properties.loginServer}/the-hunter-frontend:latest'
          resources: {
            requests: {
              cpu: 1
              memoryInGB: 1
            }
          }
          ports: [
            {
              port: 80
              protocol: 'TCP'
            }
          ]
          environmentVariables: [
            {
              name: 'API_BASE_URL'
              value: 'http://${apiContainer.properties.ipAddress.fqdn}:8000'
            }
          ]
        }
      }
    ]
    osType: 'Linux'
    restartPolicy: 'Always'
    ipAddress: {
      type: 'Public'
      dnsNameLabel: frontendContainerName
      ports: [
        {
          port: 80
          protocol: 'TCP'
        }
      ]
    }
    imageRegistryCredentials: [
      {
        server: containerRegistry.properties.loginServer
        username: containerRegistry.listCredentials().username
        password: containerRegistry.listCredentials().passwords[0].value
      }
    ]
  }
}

output frontendUrl string = 'http://${frontendContainer.properties.ipAddress.fqdn}'

// ============================================================================
// Summary Outputs
// ============================================================================
output summary object = {
  resourceGroup: resourceGroupName
  location: location
  environment: environment
  registryLoginServer: containerRegistry.properties.loginServer
  registryUsername: containerRegistry.listCredentials().username
  databaseHost: postgresServer.properties.fullyQualifiedDomainName
  databaseName: dbName
  databaseUser: dbAdminUsername
  apiContainerName: apiContainerName
  apiUrl: 'http://${apiContainer.properties.ipAddress.fqdn}:8000'
  frontendContainerName: frontendContainerName
  frontendUrl: 'http://${frontendContainer.properties.ipAddress.fqdn}'
}
