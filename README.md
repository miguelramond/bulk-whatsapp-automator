# bulk-whatsapp-automator
Whatsapp &amp; Selenium fun. Modified version of @inforkgodara's original script.

You can find the original here: https://github.com/inforkgodara/python-automated-bulk-whatsapp-messages

Although the code now seems more convoluted than the much simpler and cleaner original, the aim is to make a more robust selenium process.

### Modifications

- Added a series of dynamic wait times to allow issues with slow machines / latency / whatever to resolve themselves instead of going down a "element not found" spiral.

- Inversely, added a timeout in order to exit dynamic wait times (Implemented via 'wait.until')