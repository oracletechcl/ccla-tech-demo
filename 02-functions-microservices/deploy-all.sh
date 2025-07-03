#!/bin/bash
set -e

fn deploy --app cloudnative-workshop --local greeting-python
fn deploy --app cloudnative-workshop --local uuid-nodejs
