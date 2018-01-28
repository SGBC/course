# VM Deployment How-to

## Azure

### Creating VMs

In the azure cli, first define a few variables

```bash
my_group="enter the group name here"
vm_size="enter vm size here"
n_students="enter number of students here"
```

For the list of available sizes

```bash
az vm list-sizes --location westeurope --output table
```

Then create a VM scale set with public ips

```bash
az vmss create -n sgbc -g "${my_group}" --image ubuntults --public-ip-per-vm \
    --generate-ssh-keys --admin-username student --vm-sku "${vm_size}" \
	--instance-count "${n_students}"
```

The public IPs can be retrieved with

```bash
az vmss list-instance-public-ips --resource-group "${my_group}" --name sgbc | \
    grep "ipAddress"
```

### Connecting

Send the private key to all students and make them do the following

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
mv ~/Downloads/azure_rsa ~/.ssh
chmod 600 ~/.ssh/azure_rsa
```

They can now connect with

```bash
ssh -i ~/.ssh/azure_rsa student@ip_address
```

### Automate software installation

Install fabric

```bash
virtualenv --python=/usr/local/bin/python2.7 fab_env
source fabric/bin/activate
pip install fabric
```

Move to the `fabfiles/` dirrectory of this repo

```bash
cd fabfiles
```

then run

```bash
fab -l
```

to see available subcommands
