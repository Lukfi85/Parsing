# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instV2.items import InstItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy

class InstSubSpider(scrapy.Spider):
    name = 'inst_pars1'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'mikhailsavushkin888'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1595439927:ASxQAPm6f71xYkg1sO1NUCvXJKnguvTdc8BDs5IBnXkarlwzY88jKvzM3SnJInlUizMVuyrx4tK1LKX2w1Muu5c7/Appzx7OnmG2IRibY/m5X5IvIV2tLDC5JDA6syPphyGIYxBcFCz+TNnutkQ='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['lukfi','joteruso']
    graphql_url='https://www.instagram.com/graphql/query/?'
    folowers_hash = 'c76146de99bb02f6415203be841dd25a'
    subscribe_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response):
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':self.fetch_csrf_token(response.text)}

        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)


        if j_body['authenticated']:

            for user in self.parse_user:
                yield response.follow(
                f'/{user}',
                callback= self.folower_pars,
                cb_kwargs={'username':user}
                )


    def folower_pars(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text,username)
        variables = {"id": user_id,
                     "include_reel": True,
                     "fetch_mutual": True,
                     "first": 50}

        url_followers = f'{self.graphql_url}query_hash={self.folowers_hash}&{urlencode(variables)}'

        yield response.follow(
            url_followers,
            callback=self.user_followers_pars,
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}
        )

        url_follow = f'{self.graphql_url}query_hash={self.subscribe_hash}&{urlencode(variables)}'

        yield response.follow(
            url_follow,
            callback=self.user_follow_pars,
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}
        )



    def user_followers_pars(self, response:HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_followers = f'{self.graphql_url}query_hash={self.folowers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followers,
                callback=self.user_followers_pars,
                cb_kwargs={'username':username,
                           'user_id':user_id,
                           'variables':deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')
        for follower in followers:
            item = InstItem(
                user_parse_id=user_id,
                inst_id=follower['node']['id'],
                photo_link=follower['node']['profile_pic_url'],
                is_private=follower['node']['is_private'],
                type='followers',
                parse_user_name=username
            )

            yield item

    def user_follow_pars(self, response:HtmlResponse, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_follow = f'{self.graphql_url}query_hash={self.subscribe_hash}&{urlencode(variables)}'
            yield response.follow(
                url_follow,
                callback=self.user_follow_pars,
                cb_kwargs={'username':username,
                           'user_id':user_id,
                           'variables':deepcopy(variables)}
            )
        follow = j_data.get('data').get('user').get('edge_follow').get('edges')

        for sub in follow:

            item = InstItem(
                user_parse_id=user_id,
                inst_id=sub['node']['id'],
                photo_link=sub['node']['profile_pic_url'],
                is_private=sub['node']['is_private'],
                type='subscribe',
                parse_user_name=username
            )
            yield item


    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')