This program makes it easy to map physical buttons, connected to the Raspberry Pi's GPIO pins, to API end points. Details for each button are managed in a configuration file. All you really need to do is wire things up, then edit the file.

### Configuration

The actions for each button need to be defined in a file named: `config.yml`. Create this file inside the root of `/Pi-Magic-Button`. Here is what an example file might look like:

~~~yaml
success_pin: 17
failure_pin: 22
actions:
    - button_pin: 4
      api_url: https://www.something.com/api/blah
      api_method: POST
      api_data:
        some_field: 122345
        some_other_field: some string data
    - button_pin: 18
      api_url: https://www.something.com/api/test
      api_method: POST
      api_data:
        a_different_field: 77777
        another different_field: some string data
~~~

* `succes_pin`: This pin can be connected to an LED that will light up if the button's action successfully contacted the API end point.
* `failure_pin`: This pin can be connected to an LED that will light up if the button's action did not successfully contact the API end point.
* `actions`: This is an array of configurations corresponding to each button that has been wired up to the Raspberry Pi.


### Upstart

[Upstart](http://upstart.ubuntu.com/) is used to run this program in the background on the Raspberry Pi. It will automatically start on boot as well. Every time you edit the `config.yml` you will need to restart the `magic-button` service so that it can load the new configurations. Use this command to do that:

```
sudo service magic-button restart
```

If you ever need to completely stop the service from running you can use this command:

```
sudo service magic-button stop
```

To start it back up again, use this:

```
sudo service magic-button start
```


### TODO

* Add an install script to do all the boring setup stuff
* Add real documentation once things are settled
