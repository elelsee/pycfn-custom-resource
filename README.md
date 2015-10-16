# lambda-customresource
A helper object to create AWS Cloudformation Lambda-backed CustomResources in python

Please see example in handler.py. Update example.template accordingly.

``` shell
./build_lambda_zip.sh
aws s3 cp ./handler.zip s3://bucket/prefix/
aws s3 cp ./example.template s3://bucket/prefix/
aws cloudformation create-stack --stack-name somestack \
    --template-url https://s3.amazonaws.com/bucket/prefix/example.template \
    --capabilities CAPABILITY_IAM
```

### Example
``` python
import customresource
import logging
log = logging.getLogger()
log.setLevel(logging.INFO)

class myCustomResource(customresource.CustomResource):
    """Example of how to override the methods for Resource Events"""
    def __init__(self, event):
        super(DevCustomResource, self).__init__(event)

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
