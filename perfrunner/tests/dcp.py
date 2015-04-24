
from perfrunner.tests import PerfTest
from perfrunner.helpers.cbmonitor import with_stats
from perfrunner.workloads.viewgen import ViewGen
from perfrunner.tests.index import IndexTest
from perfrunner.tests.xdcr import XdcrTest

class ReplicationTest(PerfTest):

    COLLECTORS = {'replicate_latency': True}

    @with_stats
    def access(self):
        super(ReplicationTest, self).timer()

    def run(self):
        self.load()
        self.wait_for_persistence()

        self.compact_bucket()

        self.hot_load()

        self.workload = self.test_config.access_settings
        self.access_bg()
        self.access()

class ViewTest(IndexTest):

    COLLECTORS = {'replicate_latency': True}

    def __init__(self, *args):
        super(ViewTest, self).__init__(*args)

    @with_stats
    def access(self):
        super(ViewTest, self).timer()

    def run(self):
        self.load()
        self.wait_for_persistence()
        self.define_ddocs()
        self.build_index()
        self.compact_bucket()

        self.workload = self.test_config.access_settings
        self.access_bg()
	self.access() 
	
class DcpXdcrTest(XdcrTest):

    COLLECTORS = {'replicate_latency': True}

    def __init__(self, *args):
        super(DcpXdcrTest, self).__init__(*args)

    @with_stats
    def access(self):
        super(DcpXdcrTest, self).timer()

    def run(self):
        self.load()
        self.wait_for_persistence()

        print "enable xdcr start"
        self.enable_xdcr()
        print "enable xdcr end"
        self.compact_bucket()

        self.workload = self.test_config.access_settings
        self.access_bg()
	self.access() 
