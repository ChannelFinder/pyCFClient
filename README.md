# pyCFClient

A python client library for ChannelFinder.

## Configuration

The python channelfinder client library can be configured by setting up a `channelfinderapi.conf` file in the following locations

`/etc/channelfinderapi.conf`    
`~/.channelfinderapi.conf`   
`channelfinderapi.conf`  

The example preferences:  

```
cat ~/channelfinderapi.conf  
[DEFAULT]  
BaseURL=http://localhost:8080/ChannelFinder  
username=MyUserName  
password=MyPassword  
```
 
## Development

To install with dependancies for testing.

```bash
python -m pip install --upgrade pip
python -m pip install '.[test]'
python -m pip install .
```

### Testing

Some of the tests use docker to run a test ChannelFinderService, so a working docker installation needs to available for tests to be successful.

To run all tests:

```bash
python -m unittest discover -v -s test -p "test*.py"
```