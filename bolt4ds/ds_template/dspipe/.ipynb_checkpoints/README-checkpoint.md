# bolt4ds.flow - Project Templates
## Clean and scalable project structure for data science projects

Templates with common design patterns for https://github.com/leepand/bolt4ds/flow

## Structure

`task.py`: workflow tasks  
`cfg.py`: parameter and other config  
`run.py`: execute workflow tasks  
`visualize.py`: use outputs for further analysis  
`visualize.ipynb`: use outputs in jupyter notebook  
`.creds.yaml`: optional file with protected credentials in [yaml format](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html), not commited to git to protect credentials  

## Clean branch

For repeat usage you don't need all those comments and can use the clean branch. Clone into an existing folder using `git clone -b clean --single-branch https://github.com/leepand/bolt4ds/ds_template.git .`
