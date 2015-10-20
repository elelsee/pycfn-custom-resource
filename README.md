# pycfn-custom-resource
A helper object to create AWS Cloudformation Lambda-backed CustomResources in python

Please see [pycfn_elasticsearch](https://github.com/elelsee/pycfn-elasticsearch) for an example.

### Example
``` python
from pycfn_custom_resource.lambda_backed import CustomResource

class myCustomResource(CustomResource):
    """Example of how to override the methods for Resource Events"""
    def __init__(self, event):
        super(myCustomResource, self).__init__(event)

    def create(self):
        # Results dict referenced by GetAtt in template
        results = { "key1" : "val1" }
        return results

    def update(self):
        results = { "key1" : "val1" }
        return results

    def delete(self):
        # Delete operations do not return result data
        return None
      

def lambda_handler(event, context):
    resource = myCustomResource(event)
    resource.process_event()
    return { 'message': 'done' }
```
