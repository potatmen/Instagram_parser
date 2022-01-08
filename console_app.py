from Instagram_parser import InstagramBot
import argparse

parser = argparse.ArgumentParser(
    description="Hello, this is Instagram parser.")

parser.add_argument("--like_post", dest="like_post", type=str, default='-',
                    help='If you want to like exact post: --like_post "post url"')
parser.add_argument("--like_all", dest="like_all", type=str, default='-',
                    help='If you want to like all post of user: --like_all "user url"')
parser.add_argument("--download_all", dest="download_all", type=str, default='',
                    help='If you want to download all photos of user: --download_all "user url"')
args = parser.parse_args()


bot = InstagramBot()
bot.login()
if args.like_post != '-':
    bot.put_exact_like(args.like_post)
elif args.like_all != '-':
    bot.likes_for_all_posts(args.like_all)
else:
    bot.download_content_from_user(args.download_all)
print('Everything is done!')
