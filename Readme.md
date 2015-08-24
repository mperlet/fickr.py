## fickr
> download all public flickr-photos from a user

## Installation

    pip install fickr

    git clone git@github.com:mperlet/fickr.py.git



## Usage

    fickr <username> <size>

## Sizes

* *sq* Square 75 (75 x 75)
* *q*  Square 150 (150 x 150)
* *t*  Thumbnail (100 x 56)
* *s*  Small 240
* *n*  Small 320
* *m*  Medium 500
* *z*  Medium 640
* *c*  Medium 800
* *l*  Large 1024
* *q*  Large 1600
* *k*  Large 2048
* *o*  Original

## Example

    # download original picture size
    python fickr mperlet

    # download thumbnail size
    python fickr mperlet t
