import util
import requests
import json
import uuid
import sys
import traceback
import boto3
from time import sleep

import logging
log = logging.getLogger()
log.addHandler(logging.NullHandler())
log.setLevel(logging.DEBUG)


_DEFAULT_CREATE_TIMEOUT = 30 * 60
_DEFAULT_DELETE_TIMEOUT = 30 * 60
_DEFAULT_UPDATE_TIMEOUT = 30 * 60


class CustomResource(object):
    def __init__(self, event, context):
        self._event = event
        self._context = context
        self._logicalresourceid = event.get("LogicalResourceId")
        self._physicalresourceid = event.get("PhysicalResourceId")
        self._requestid = event.get("RequestId")
        self._resourceproperties = event.get("ResourceProperties")
        self._resourcetype = event.get("ResourceType")
        self._responseurl = event.get("ResponseURL")
        self._requesttype = event.get("RequestType")
        self._servicetoken = event.get("ServiceToken")
        self._stackid = event.get("StackId")
        self._stackname = self._get_stackname()
        self._region = self._get_region()
        self.result_text = event.get("Data")
        self.result_attributes = {}
        self.processing = True if self.result_text else False

        # Set timeout for actions
        self._create_timeout = _DEFAULT_CREATE_TIMEOUT
        self._delete_timeout = _DEFAULT_DELETE_TIMEOUT
        self._update_timeout = _DEFAULT_UPDATE_TIMEOUT

    @property
    def logicalresourceid(self):
        return self._logicalresourceid

    @property
    def physicalresourceid(self):
        return self._physicalresourceid

    @property
    def requestid(self):
        return self._requestid

    @property
    def resourceproperties(self):
        return self._resourceproperties

    @property
    def resourcetype(self):
        return self._resourcetype

    @property
    def responseurl(self):
        return self._responseurl

    @property
    def requesttype(self):
        return self._requesttype

    @property
    def servicetoken(self):
        return self._servicetoken

    @property
    def stackid(self):
        return self._stackid

    def create(self):
        return {}

    def delete(self):
        return {}

    def update(self):
        return {}

    def _get_region(self):
        if 'Region' in self._resourceproperties:
            return self._resourceproperties['Region']
        else: 
            return self._stackid.split(':')[3]

    def _get_stackname(self):
        return self.stackid.split(':')[-1].split('/')[1]

    def _get_source_attributes(self, success):
        source_attributes = {
            "Status": 
                "SUCCESS" if success else "FAILED",
            "StackId": 
                self.stackid,
            "RequestId": 
                self.requestid,
            "LogicalResourceId": 
                self.logicalresourceid,
            "PhysicalResourceId": 
                self.physicalresourceid if self.physicalresourceid else str(uuid.uuid4())
        }
        return source_attributes

    def invoke_chained_lambda(self):
        log.info(u"Invoking chained lambda %s-%s", self.logicalresourceid, self.requesttype)
        source_attributes = self._get_source_attributes(True)
        source_attributes.update(self._event)
        source_attributes.update(self.result_attributes)
        client = boto3.client('lambda')
        response = client.invoke(
            FunctionName=self._context.function_name,
            InvocationType='Event',
            Payload=json.dumps(source_attributes),
            Qualifier=self._context.function_version
        )

    def process_event(self):
        if self.requesttype == "Create":
            command = self.create
        elif self.requesttype == "Delete":
            command = self.delete
        elif self.requesttype == "Update":
            command = self.update

        try:
            self.result_text = command()
            success = True
            try:
                self.result_attributes = { "Data" : self.result_text }
                log.info(u"Command %s-%s succeeded", self.logicalresourceid, self.requesttype)
                log.debug(u"Command %s output: %s", self.logicalresourceid, self.result_text)
            except:
                log.error(u"Command %s-%s returned invalid data: %s", self.logicalresourceid,
                          self.requesttype, self.result_text)
                success = False

        except:
            e = sys.exc_info()
            log.error(u"Command %s-%s failed", self.logicalresourceid, self.requesttype)
            log.debug(u"Command %s error: %s", self.logicalresourceid, str(e[1]))
            log.debug(u"Command %s traceback:", self.logicalresourceid)
            traceback.print_tb(e[2])
            success = False

        log.debug(u"Command %s-%s processing %s", self.logicalresourceid, self.requesttype, self.processing)
        log.debug(u"Command %s-%s success %s", self.logicalresourceid, self.requesttype, success)
        if self.processing and success:
            log.info(u"Command %s-%s sleeping for 60 seconds", self.logicalresourceid, self.requesttype)
            sleep(60)
            self.invoke_chained_lambda()
        else:
            self.send_result(success)
        log.info(u"Command %s-%s processing completed", self.logicalresourceid, self.requesttype)

    def send_result(self, success):
        source_attributes = self._get_source_attributes(success)
        source_attributes.update(self.result_attributes)
        log.debug(u"Sending result: %s", source_attributes)
        self._put_response(source_attributes)

    @util.retry_on_failure(max_tries=10)
    def __send(self, data):
        requests.put(self.responseurl,
                     data=json.dumps(data),
                     headers={"Content-Type": ""},
                     verify=True).raise_for_status()

    def _put_response(self, data):
        try:
            self.__send(data)
            log.info(u"CloudFormation successfully sent response %s", data["Status"])
        except IOError, e:
            log.exception(u"Failed sending CloudFormation response")

    def __repr__(self):
        return str(self._event)
