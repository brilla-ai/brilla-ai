**Colab Version Control**

In line with best practices, developers using Google colaboratory to write their scripts are encouraged to integrate their notebooks into Github for version control.

**Steps to integrate Colab with Github**
1. Clone the nsmqai repositiory and create a local branch. All branches must have the right naming conventions. See [here](https://github.com/nsmq-ai/nsmqai/blob/34bca778b61e3cca6532805c37eae9e74d18a8a5/docs/CONTRIBUTING.md) for more information on how to name your branch.
2. Push the local branch with no new changes to Github in order to create a remote branch. 
3. Open your notebook in Google Colaboratory.
4. Click on 'File' and select 'Save a copy in Github'.
5. A pop up window will appear and you will be asked to authenticate your Google account with your Github account if you haven't already done so.
6. After authentication, select 'nsmq-ai/nsmqai' in the drop down arrow next to repository.
7. Click on the drop down arrow next to branch and select the branch you have created.
8. Write a commit message for your change.
9. Select 'Include a link to Colaboratoy' if you want your script to be opened in Google Colab directly from Github.
10. Click on 'Ok' when you are done.


Your script will be pushed to the branch you created now. You may go ahead to create a PR when you are ready to merge your changes to the main branch.

**NB**

After you have saved a copy of your notebook in Github and you make any further changes to your notebook, you would have to save a copy again to the same branch in order for your new changes to reflect.
