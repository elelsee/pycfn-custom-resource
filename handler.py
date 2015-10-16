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
