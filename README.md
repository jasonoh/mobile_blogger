# mobile_blogger
This is a [Pythonista](http://omz-software.com/pythonista/) script that integrates with the iOS share panel to allow you to:
* use your favorite iOS markdown editor to create Jekyll posts
* automatically create the YAML front-matter for these posts using the post's main header and text input
* automatically commit these files to a [Gitlab](https://gitlab) repo (yes, Gitlab—I don't use the Jekyll integration with Github)
* automatically sync these files to a designated location in Dropbox

The config file let's you specify Gitlab and Dropbox deets.

This is largely based on the [work](http://codenugget.co/2015/11/18/mobile-blogging-with-pythonista-jekyll-and-github.html) from Pascal Cremer, but updated for Gitlab (vs Github) and with the added integration with Dropbox.

## Details
My Jekyll instance resides on my own server, so I don't rely on the Github feature for hosting my blog. Git commits are
so that I have versioning on my blog posts. The key for my setup is the headless Dropbox instance on my server; once I sync
the relevant file to the appropriate location in Dropbox, it automatically syncs to the server and the post goes live.

Your setup may be entirely different and this application may not suit your needs at all.

Feel free to contribute comments/improvements!

# License
This application is free for use under the [MIT license](http://opensource.org/licenses/mit-license.php).
