
from perfrunner.tests import PerfTest, TargetIterator
from perfrunner.helpers.cbmonitor import with_stats
from perfrunner.workloads.viewgen import ViewGen
from perfrunner.tests.index import IndexTest
from perfrunner.helpers.misc import log_phase, target_hash
from perfrunner.settings import TargetSettings

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
