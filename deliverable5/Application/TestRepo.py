import unittest
import repo

class TestRepo(unittest.TestCase): 

     def setUp(self):
          repo.changeLocalRepo("C:\\Users\\den_t\\Documents\\GitHub\\team25-Project\\deliverable5\\Application")
          
     def test_getLocalRepo(self):
          self.assertEqual(repo.getLocalRepo(), "C:\\Users\\den_t\\Documents\\GitHub\\team25-Project\\deliverable5\\Application", "Wrong path returned")
        
     def test_changeLocalRepo(self):
          repo.changeLocalRepo("C:\\Users\\den_t\\Documents\\GitHub\\team25-Project\\deliverable5")
          self.assertEqual(repo.getLocalRepo(), "C:\\Users\\den_t\\Documents\\GitHub\\team25-Project\\deliverable5", "Did not correctly change the repo")
          
     def test_changeLocalRepoEmpty(self):
          repo.changeLocalRepo("")
          self.assertEqual(repo.getLocalRepo(), "", "Repo should now be empty")   
     
if __name__ == '__main__':
     unittest.main(exit=False)