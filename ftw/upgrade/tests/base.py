from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class WorkflowTestCase(TestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def assertReviewStates(self, expected):
        wftool = getToolByName(self.portal, 'portal_workflow')

        got = {}
        for obj in expected.keys():
            review_state = wftool.getInfoFor(obj, 'review_state')
            got[obj] = review_state

        self.assertEquals(
            expected, got, 'Unexpected workflow states')

    def set_workflow_chain(self, for_type, to_workflow):
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes((for_type,),
                                      (to_workflow,))

    def assertSecurityIsUpToDate(self):
        wftool = getToolByName(self.portal, 'portal_workflow')
        updated_objects = wftool.updateRoleMappings()
        self.assertEquals(
            0, updated_objects,
            'Expected all objects to have an up to date security, but'
            ' there were some which were not up to date.')

    def get_allowed_roles_and_users(self, for_object):
        catalog = getToolByName(self.portal, 'portal_catalog')
        path = '/'.join(for_object.getPhysicalPath())
        rid = catalog.getrid(path)
        index_data = catalog.getIndexDataForRID(rid)
        return index_data.get('allowedRolesAndUsers')

    def create_placeful_workflow_policy(self, named, with_workflows):
        placeful_wf_tool = getToolByName(
            self.portal, 'portal_placeful_workflow')

        placeful_wf_tool.manage_addWorkflowPolicy(named)
        policy = placeful_wf_tool.get(named)

        for portal_type, workflow in with_workflows.items():
            policy.setChain(portal_type, workflow)

        return policy
