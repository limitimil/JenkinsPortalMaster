# -*- encoding: utf-8 -*-
import unittest
from jira_services.jira_markdown_helper import JiraMarkdownHelper
RAW_MARKDWON="""
* *helloworld:*
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
* *hellohell:*
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
"""
AGGREGATED_MARKDWON="""
* *helloworld:*(10+)
* *hellohell:*
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
** [http://google.com|http://google.com] 
"""
class TestJiraMarkdownHelper(unittest.TestCase):
    def test_aggregate_content(self):
        jmh = JiraMarkdownHelper(RAW_MARKDWON)
        result = jmh.aggregate_content('helloworld')
        self.assertEqual(result , AGGREGATED_MARKDWON)

        jmh = JiraMarkdownHelper(TEST_DATA_2)
        result = jmh.aggregate_content('helloworld')
        self.assertEqual(result , EXPECTED_RESULT_2)


if __name__ == '__main__':
    unittest.main()

