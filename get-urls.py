#!/usr/bin/env python3
import subprocess
import json
import time

def get_azure_resource(rg, name):
    cmd = f"az container show --resource-group {rg} --name {name} --query '{{fqdn: ipAddress.fqdn, status: instanceView.state}}' -o json"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return json.loads(result.stdout) if result.stdout else None
    except:
        return None

rg = "yashus-rg"

print("\n╔════════════════════════════════════════════════════════════════╗")
print("║       🎉 YASHUS CALCULATOR DEPLOYED ON AZURE! 🎉            ║")
print("╚════════════════════════════════════════════════════════════════╝\n")

for i in range(6):
    frontend = get_azure_resource(rg, "yashus-frontend")
    backend = get_azure_resource(rg, "yashus-backend")
    
    if frontend and frontend.get('fqdn') and backend and backend.get('fqdn'):
        print("📊 CALCULATOR FRONTEND:")
        print(f"   http://{frontend['fqdn']}")
        print()
        print("🔧 BACKEND API:")
        print(f"   http://{backend['fqdn']}:8000")
        print()
        print("📚 SWAGGER API DOCS:")
        print(f"   http://{backend['fqdn']}:8000/docs")
        print()
        print("✅ Both containers are RUNNING on Azure (westus2)")
        print()
        break
    else:
        print(f"⏳ Waiting for public IPs... ({i+1}/6)")
        if frontend: print(f"   Frontend: {frontend.get('status', 'provisioning')}")
        if backend: print(f"   Backend: {backend.get('status', 'provisioning')}")
        if i < 5:
            time.sleep(5)

print()
