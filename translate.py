#!/usr/bin/python3

import googletrans
import sys
import argparse

def get_config():
	with open('config', 'r') as f:
		lines = f.read().splitlines()

	cfg = {}
	for line in lines:
		if line.startswith('#') or line.startswith('['):
			continue
		data = line.split()
		if '=' in data and len(data) == 3:
			cfg[data[0]] = data[2]

	return cfg

def get_lang(res):
	lang = []
	src = res.src
	dst = res.dest
	if src in googletrans.LANGUAGES:
		lang.append(googletrans.LANGUAGES[src])
		lang.append(src)
	else:
		lang.append(src)
		lang.append(googletrans.LANGCODES[src])

	if dst in googletrans.LANGUAGES:
		lang.append(googletrans.LANGUAGES[dst])
		lang.append(dst)
	else:
		lang.append(dst)
		lang.append(googletrans.LANGCODES[dst])

	return lang

def main(trans, args):
	cfg = get_config()
	verbose = []
	dst = 'en'

	if args.dst:
		dst = args.dst
	else:
		if 'dst' in cfg:
			dst = cfg['dst']
		else:
			verbose.append('Default "dst" not found in config, using "en"')

	if dst in googletrans.LANGUAGES or args.dst in googletrans.LANGCODES:
		dest = dst
	else:
		print(f"Error: {dst} is not present in supported languages.")
		sys.exit(1)

	res = trans.translate(args.text, dest=dest)

	if args.v or ('v' in cfg and cfg['v'] == 'True'):
		lang = get_lang(res)
		verbose.append("{}[{}] => {}[{}]".format(lang[0], lang[1], lang[2], lang[3]))
		for vb in verbose:
			print(vb)

	if args.p or ('p' in cfg and cfg['p'] == 'True'):
		print("[TEXT] {}".format(res.text))
		print("[PRON] {}".format(res.pronunciation))
	else:
		print("{}".format(res.text))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="Translate text from one language to another language",
		epilog="Note: This script uses 'googletrans' for translation of text")
	parser.add_argument('text', help='The text to be translated')
	parser.add_argument('-p', help='Show pronunciation in English (en)', action='store_true', default=False)
	parser.add_argument('-v', help='Display more data', action='store_true', default=False)
	parser.add_argument('--dst', help='Translate text to the given language (lang code / lang name)')
	args = parser.parse_args()

	trans = googletrans.Translator()
	main(trans, args)