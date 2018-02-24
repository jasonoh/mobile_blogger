### Mobile Blogging Integration for iOS (Pythonista) + Editorial + Gitlab + Dropbox

![alt text](https://img.shields.io/badge/Python-3.6-blue.svg "Python 3.6")

### Prerequisites
* [Pythonista for iOS](http://omz-software.com/pythonista/)
* [Gitlab](https://gitlab.com)
  * generate a [personal access token](https://gitlab.com/profile/personal_access_tokens)
  * obtain the project id for the associated repo by running the following command, replacing <YOUR PRIVATE TOKEN> with your Gitlab private token and <YOUR USERNAME> with your Gitlab username:
    * `%> curl -XGET --header "PRIVATE-TOKEN: <YOUR PRIVATE TOKEN>" "https://gitlab.com/api/v4/users/<YOUR USERNAME>/projects" | python -mjson.tool`
    * then find the "id" for the relevant project&mdash;you'll need this for the `post[gitlab_repo]` config in `config.py`

### Overview
This is a [Pythonista](http://omz-software.com/pythonista/) script that integrates with the iOS share panel to allow you to use your favorite iOS markdown editor to create Jekyll posts and automate the following:
* Creation the YAML front-matter for these posts using the post's main header and text input
* Committing your post to your [Gitlab](https://gitlab.com) repo. Yes, the irony of using Gitlab as an integration point for a Github project isn't lost on me, however, there are 2 reasons for this:
  * I don't use the built-in Jekyll integration with Github projects 
  * I prefer to have my blog artifacts private and Github doesn't permit private repos for free accounts
* Syncing files from repo to Dropbox

This is largely based on the [work](http://codenugget.co/2015/11/18/mobile-blogging-with-pythonista-jekyll-and-github.html) from Pascal Cremer, but updated for Gitlab (vs Github) and with the added integration with Dropbox.

### Assumptions
* Your Jekyll folder is stored in Dropbox ("Content Source") and is the basis from which your Jekyll instance generates your static site
* Content Source is a Git project and hosted in Gitlab
* You have shell access to a server with the Dropbox CLI [client](https://www.dropbox.com/install-linux) 

### Workflow
* Write your blog post in Markdown (or Kramdown) in your favorite iOS editor (I use [Editorial](http://omz-software.com/editorial/index.html))
* Click the Share option and run the Pythonista Share Extension Shortcut associated with this script
* Enter the front-matter details in the UI form
* Click Done; this will commit the post to your Gitlab repo, sync it to Dropbox and update

### Notes
This integration commits the post to Gitlab and then syncs 

### See it Live
My [website](https://jasonoh.org) is built using Jekyll and posts are created using [Editorial](http://omz-software.com/editorial/) and this integration. 

Feel free to contribute comments/improvements!
