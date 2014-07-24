This program makes it easy to map physical buttons, connected to the Raspberry Pi's GPIO pins, to API end points. Details for each button are managed in a configuration file. All you really need to do is wire things up, then edit the file.

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
