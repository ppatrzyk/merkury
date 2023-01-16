# gh-pages docs

```
sudo docker run --rm -it -v $PWD:/srv/jekyll -p 4000:4000 jekyll/jekyll:4.2.2 bash
jekyll serve -c _config_local.yml -H 0.0.0.0
```
