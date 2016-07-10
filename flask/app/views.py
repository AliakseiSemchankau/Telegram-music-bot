from flask import render_template, flash, redirect
from app import app
from .forms import *
import psycopg2


SQL_SIMILAR_BANDS_ON_BAND = '''
SELECT *
FROM choose_similar_bands(%s)
'''

SQL_SIMILAR_BANDS_ON_BAND_TRACK = '''
SELECT *
FROM choose_similar_bands(%s, %s)
'''

SQL_SIMILAR_TRACKS_ON_BAND = '''
SELECT *
FROM choose_similar_tracks(%s)
'''

SQL_SIMILAR_TRACKS_ON_BAND_TRACK = '''
SELECT *
FROM choose_similar_tracks(%s, %s)
'''

SQL_POSTS_WITH_BAND_ONLY_ON_BAND = '''
SELECT *
FROM choose_nonmixes_with_band(%s)'''

SQL_POSTS_WITH_BAND_MIXES_ON_BAND = '''

SELECT *
FROM choose_mixes_with_band(%s)
'''

SQL_POSTS_WITH_BAND_ONLY_ON_BAND_TRACK = '''
SELECT *
FROM choose_posts_with_track(%s, %s)
'''

SQL_POSTS_WITH_BAND_MIXES_ON_BAND_TRACK = '''
SELECT *
FROM choose_posts_with_track(%s, %s)
'''

def normalize_limit(limit):
    try:
        limit = int(limit)
    except:
        limit = 20

    limit = limit + 1
    if limit < 0:
        limit = 0
    if limit > 300:
        limit = 300
    return limit

@app.route('/base', methods=['GET', 'POST'])
def base():
    similars_form = SimilarsForm()
    posts_with_band_form = PostsWithBandForm()
    kwargs = {'similars_form': similars_form, 'posts_with_band_form': posts_with_band_form}

    return render_template('ind.html', **kwargs)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():

    print ('zdraste')

    similars_form = SimilarsForm()
    vk_posts_form = VkPostsForm()

    kwargs = {'similars_form': similars_form, 'vk_posts_form': vk_posts_form}

    if similars_form.validate_on_submit():

        sb_band = str(similars_form.sb_band.data).lower()
        sb_track = str(similars_form.sb_track.data).lower()
        sb_limit = similars_form.sb_limit.data
        sb_limit = normalize_limit(sb_limit)
        sb_pref = str(similars_form.sb_pref.data)

        print ('sb_track=', sb_track)
        print (sb_track)

        conn = psycopg2.connect(database="mydb", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        cursor = conn.cursor()

        if len(sb_track) < 2:
            if sb_pref == 'pref_bands':
                sql = SQL_SIMILAR_BANDS_ON_BAND % ("'" + sb_band + "'")
            else:
                sql = SQL_SIMILAR_TRACKS_ON_BAND % ("'" + sb_band + "'")
        else:
            if sb_pref == 'pref_bands':
                sql = SQL_SIMILAR_BANDS_ON_BAND_TRACK % ("'" + sb_band+ "'", "'" + sb_track + "'")
            else:
                sql = SQL_SIMILAR_TRACKS_ON_BAND_TRACK % ("'" + sb_band + "'", "'" + sb_track + "'")

        cursor.execute(sql)

        sb_results = cursor.fetchall()

        for sb_result in sb_results:
            print (sb_result)

        sb_limit = min(len(sb_results), sb_limit)
        sb_results = sb_results[1:sb_limit]

        kwargs['similars_results'] = sb_results
        kwargs['similar_form_band'] = sb_band

        return render_template("ind.html", **kwargs)

    if vk_posts_form.validate_on_submit():

        vp_band = str(vk_posts_form.vp_band.data).lower()
        vp_track = str(vk_posts_form.vp_track.data).lower()
        vp_limit = vk_posts_form.vp_limit.data
        vp_limit = normalize_limit(vp_limit)
        vp_pref = str(vk_posts_form.vp_pref.data)

        print ('vp_track=', vp_track)
        print (vp_track)

        conn = psycopg2.connect(database="mydb", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        cursor = conn.cursor()

        if len(vp_track) < 2:
            if vp_pref == 'only_band':
                sql = SQL_POSTS_WITH_BAND_ONLY_ON_BAND % ("'" + vp_band + "'")
            else:
                sql = SQL_POSTS_WITH_BAND_MIXES_ON_BAND % ("'" + vp_band + "'")
        else:
            if vp_pref == 'only_band':
                sql = SQL_POSTS_WITH_BAND_ONLY_ON_BAND_TRACK % ("'" + vp_band + "'", "'" + vp_track + "'")
            else:
                sql = SQL_POSTS_WITH_BAND_MIXES_ON_BAND_TRACK % ("'" + vp_band + "'", "'" + vp_track + "'")

        cursor.execute(sql)

        vp_results = cursor.fetchall()

        for vp_result in vp_results:
            print (vp_result)

        vp_limit = min(len(vp_results), vp_limit)
        vp_results = vp_results[1:vp_limit]

        kwargs['vp_results'] = vp_results
        kwargs['vp_form_band'] = vp_band

        return render_template("ind.html", **kwargs)

    return render_template("ind.html", **kwargs)



