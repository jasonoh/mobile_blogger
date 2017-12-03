### Mobile Blogging Integration for iOS (Pythonista) + Editorial + Gitlab + Dropbox

![alt text](https://img.shields.io/badge/Python-3.6-blue.svg "Python 3.6")

### Prerequisites
* [Pythonista for iOS](http://omz-software.com/pythonista/)
* [Gitlab](https://gitlab.com)
  * generate a (personal access token)[https://gitlab.com/profile/personal_access_tokens]
  * obtain the project id for the associated repo
* [Dropbox](https://dropbox.com)
  * create a Dropbox app for this integration

### Overview
This is a [Pythonista](http://omz-software.com/pythonista/) script that integrates with the iOS share panel to allow you to:
* use your favorite iOS markdown editor to create Jekyll posts
* automatically create the YAML front-matter for these posts using the post's main header and text input
* automatically commit these files to a [Gitlab](https://gitlab.com) repo (yes, Gitlab—I don't use the Jekyll integration with Github)
* automatically sync these files to a designated location in Dropbox

The config file let's you specify Gitlab and Dropbox deets.

This is largely based on the [work](http://codenugget.co/2015/11/18/mobile-blogging-with-pythonista-jekyll-and-github.html) from Pascal Cremer, but updated for Gitlab (vs Github) and with the added integration with Dropbox.


### Workflow
* Write your blog post in Markdown (or Kramdown) in your favorite iOS editor (I use [Editorial](http://omz-software.com/editorial/index.html))
* Click the Share option and run the Pythonista Share Extension Shortcut associated with this script
* Enter the front-matter details in the UI form
* Click Done; this will commit the post to your Gitlab repo and sync it to Dropbox

### Details
My Jekyll instance resides on my own server, so I don't rely on the Github feature for hosting my blog. Git commits are
so that I have versioning on my blog posts and don't serve as the mechanism for publishing. The key for my setup is the headless Dropbox instance on my server; once I sync the relevant file to the appropriate location in Dropbox, it automatically syncs to the server and the post goes live. As such, this assumes that you are using Dropbox as a store for your Jekyll installation and are detecting changes on your server for auto-publishing.

Your setup may be entirely different and this application may not suit your needs at all.

Feel free to contribute comments/improvements!
