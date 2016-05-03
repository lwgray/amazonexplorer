__author__ = 'lwgra_000'
from boto.mws.connection import MWSConnection
import os
import socket
import time
from boto.s3.connection import S3Connection
from boto.s3.key import Key


Append = list.append
socket.setdefaulttimeout(5)
ID = os.environ.get('MWS_ACCESS_KEY_ID')
SECRET = os.environ.get('MWS_SECRET_ACCESS_KEY')
SIMPLE = os.environ.get('MWS_SIMPLE')
SHACK = os.environ.get('MWS_SHACK')
AWSACCESS = os.environ.get('AWS_ID')
AWSSECRET = os.environ.get('AWS_KEY')


class Build(object):
    def __init__(self, ReportType):
        self.simple = SIMPLE
        self.shack = SHACK
        self.mws = MWSConnection(Merchant=self.simple,
                                 aws_access_key_id=ID,
                                 aws_secret_access_key=SECRET)
        self.ProcessingStatus = None
        # self.ReportType = '_GET_FBA_MYI_ALL_INVENTORY_DATA_'
        self.ReportType = ReportType
        self.Report = None
        self.GeneratedReportId = None
        self.hasNext = False
        self.nextToken = None
        self.ReportRequestList = None
        self.ReportList = None
        self.ReportRequestId = None

    def get_report(self):
        # Step 1 request report
        response = self.mws.request_report(MarketplaceId=self.shack,
                                           ReportType=self.ReportType)
        # Step 2 Get ReportRequestId
        self.ReportRequestId = response.RequestReportResult.\
            ReportRequestInfo.ReportRequestId
        # Step 3 Get  GetReportRequestList, Get report processing status
        # Wait untill Done
        while self.ProcessingStatus != '_DONE_' and \
                self.ProcessingStatus != '_CANCELLED_':
            self.ReportRequestList = self.mws.get_report_request_list(
                ReportRequestIdList=[self.ReportRequestId])
            self.ProcessingStatus = self.ReportRequestList.\
                GetReportRequestListResult.ReportRequestInfo[0].\
                ReportProcessingStatus
            print self.ProcessingStatus
            if self.ProcessingStatus == '_SUBMITTED_':
                time.sleep(15)
        # Step 4 - Get Generated Report Id
        if self.ProcessingStatus == '_CANCELLED_':
            self.ReportList = self.mws.get_report_list(
                ReportTypeList=[self.ReportType])
            for item in self.ReportList.GetReportListResult.ReportInfo:
                self.ReportRequestId = item.ReportRequestId
                self.ReportRequestList = self.mws.get_report_request_list(
                    ReportRequestIdList=[self.ReportRequestId])
                self.GeneratedReportId = self.ReportRequestList.\
                    GetReportRequestListResult.\
                    ReportRequestInfo[0].GeneratedReportId
                break
        else:
            self.GeneratedReportId = self.ReportRequestList.\
                GetReportRequestListResult.ReportRequestInfo[0].\
                GeneratedReportId
        # Step7 - Get Report
        self.Report = self.mws.get_report(ReportId=self.GeneratedReportId)
        # Step 8 - Process Report and save it as csv

    def write_report_data(self, name):
        if self.Report is not None:
            conn = S3Connection(AWSACCESS, AWSSECRET)
            bucket = conn.get_bucket('invntry-rprt')
            key = Key(bucket)
            key.key = '{0}_report.txt'.format(name)
            key.set_contents_from_string(self.Report)
        else:
            return "Error, No Report Found!  Please get_inventory_report First"
        return


if __name__ == '__main__':
    report = Build()
    report.get_report()
    report.write_report_data()
