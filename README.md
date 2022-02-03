# showGroups

### Description
This project shows what Linux users in what groups

In OS Linux there are files - **/etc/passwd** and **/etc/groups**, which aren't informateble if you watch these via text editors.  
So **showGroups** tris to help you to get informations about users in Linux and about participants of groups.

Moreover this project can help to synchronize users and groups in clusters. In most cases clusters are based on NFS servers.
NFS server requires synchronized UIDs and GIDs on all machines in clusters.

### Requirements
Install some Python modules - `pip3 install -r requirements`  
If you don't have pip3 then you may install it [how described here](https://pip.pypa.io/en/stable/installation/)

### Planning
#### In future this project should be helpful to deploy new machines in any clusters.
