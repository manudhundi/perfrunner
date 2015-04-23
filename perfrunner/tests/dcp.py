
from perfrunner.tests import PerfTest
from perfrunner.helpers.cbmonitor import with_stats
from perfrunner.workloads.viewgen import ViewGen
from perfrunner.tests.index import IndexTest

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
	
class XdcrTest(PerfTest):

    COLLECTORS = {'replicate_latency': True}

    def __init__(self, *args):
        super(XdcrTest, self).__init__(*args)

    @with_stats
    def access(self):
        super(XdcrTest, self).timer()

    def _start_replication(self, m1, m2):
        name = target_hash(m1, m2)
        certificate = self.settings.use_ssl and self.rest.get_certificate(m2)
        self.rest.add_remote_cluster(m1, m2, name, certificate)

        for bucket in self.test_config.buckets:
            params = {
                'replicationType': 'continuous',
                'toBucket': bucket,
                'fromBucket': bucket,
                'toCluster': name
            }
            if self.settings.replication_protocol:
                params['type'] = self.settings.replication_protocol
            self.rest.start_replication(m1, params)

    def enable_xdcr(self):
        m1, m2 = self.cluster_spec.yield_masters()

        if self.settings.replication_type == 'unidir':
            self._start_replication(m1, m2)
        if self.settings.replication_type == 'bidir':
            self._start_replication(m1, m2)
            self._start_replication(m2, m1)

    def run(self):
        self.load()
        self.wait_for_persistence()

        self.enable_xdcr()
        self.compact_bucket()

        self.workload = self.test_config.access_settings
        self.access_bg()
	self.access() 
