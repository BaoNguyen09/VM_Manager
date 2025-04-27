| Item | Value |
|------|-------|
| Provider Name | DigitalOcean |
| VM API Endpoint (for creating droplet) | https://api.digitalocean.com/v2/droplets
| Authentication Method | Bearer Token Authorization
| How to pass API Token | Add HTTP Header Authorization: Bearer <your-token>
| Default Image (OS) | Ubuntu 22.04 (image slug: ubuntu-22-04-x64)
| Default Region | sfo3
| Default Size | s-1vcpu-1gb (the $4/month one)
| API Docs | https://docs.digitalocean.com/reference/api/digitalocean/#tag/Droplets/operation/droplets_create