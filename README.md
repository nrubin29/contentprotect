# contentprotect

A platform to help protect your content from thieves and reposters on Reddit. The process works like this:

1. Upload your content (current only images are supported). ContentProtect computes a hash from the image, so the actual image isn't stored.
2. A bot will scan Reddit every hour for the images in the database. If any matches are found, they'll be logged.
3. You can see any content matches that the bot finds and take appropriate action.