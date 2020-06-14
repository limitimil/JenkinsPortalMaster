# -*- encoding: utf-8 -*-
import unittest
from jira_services.jira_markdown_helper import JiraMarkdownHelper
TEST_DATA_1="""* *helloworld:*
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
** """
EXPECTED_RESULT_1="""* *helloworld:*(10+)"""
TEST_DATA_2="""* *helloworld:*
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
* hellohell
** [http://google.com|http://google.com] 
"""
EXPECTED_RESULT_2="""* *helloworld:*(10+)
* hellohell
** [http://google.com|http://google.com] 
"""
TEST_DATA_3="""* *helloworld:*
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
* hellohell
** [http://google.com|http://google.com] 
"""
EXPECTED_RESULT_3="""* *helloworld:*(squashed)
* hellohell
** [http://google.com|http://google.com] 
"""
class TestJiraMarkdownHelper(unittest.TestCase):
    def test_squash_content(self):
        jmh = JiraMarkdownHelper(TEST_DATA_1)
        result = jmh.squash_content('helloworld', 10)
        self.assertEqual(result , EXPECTED_RESULT_1)

        jmh = JiraMarkdownHelper(TEST_DATA_2)
        result = jmh.squash_content('helloworld', 10)
        self.assertEqual(result , EXPECTED_RESULT_2)

        jmh = JiraMarkdownHelper(TEST_DATA_3)
        result = jmh.squash_content('helloworld')
        self.assertEqual(result , EXPECTED_RESULT_3)

if __name__ == '__main__':
    unittest.main()

