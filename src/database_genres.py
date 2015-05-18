#!/usr/bin/python
# Copyright (c) 2014-2015 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from gettext import gettext as _

from lollypop.define import Lp


# All functions take a sqlite cursor as last parameter,
# set another one if you're in a thread
class DatabaseGenres:
    def __init__(self):
        pass

    """
        Add a new genre to database
        @param Name as string
        @param outside as bool
        @warning: commit needed
    """
    def add(self, name, outside, sql=None):
        if not sql:
            sql = Lp.sql
        sql.execute("INSERT INTO genres (name, outside) VALUES (?, ?)",
                    (name, outside))

    """
        Get genre id for name
        @param name as string
        @return genre id as int
    """
    def get_id(self, name, sql=None):
        if not sql:
            sql = Lp.sql
        result = sql.execute("SELECT rowid FROM genres\
                              WHERE name=?", (name,))
        v = result.fetchone()
        if v:
            return v[0]

        return None

    """
        Get genre name for genre id
        @param string
        @return int
    """
    def get_name(self, genre_id, sql=None):
        if not sql:
            sql = Lp.sql
        result = sql.execute("SELECT name FROM genres\
                              WHERE rowid=?", (genre_id,))
        v = result.fetchone()
        if v:
            return v[0]

        return _("Unknown")

    """
        Get all availables albums  for genres
        @return Array of id as int
    """
    def get_albums(self, genre_id, sql=None):
        if not sql:
            sql = Lp.sql
        albums = []
        result = sql.execute("SELECT albums.rowid FROM albums, album_genres\
                             WHERE album_genres.genre_id=?\
                             AND album_genres.album_id=albums.rowid",
                             (genre_id,))
        for row in result:
            albums += row
        return albums

    """
        Get all availables genres
        @return [(id as int, name as string)]
    """
    def get(self, sql=None):
        if not sql:
            sql = Lp.sql
        genres = []
        result = sql.execute("SELECT rowid, name FROM genres\
                              ORDER BY name COLLATE NOCASE")
        for row in result:
            genres += (row,)
        return genres

    """
        Get all availables genres ids
        @return [id as int]
    """
    def get_ids(self, sql=None):
        if not sql:
            sql = Lp.sql
        genres = []
        result = sql.execute("SELECT rowid FROM genres\
                              ORDER BY name COLLATE NOCASE")
        for row in result:
            genres += (row)
        return genres

    """
        Clean database for genre id
        @param genre id as int
        @warning commit needed
    """
    def clean(self, genre_id, sql=None):
        if not sql:
            sql = Lp.sql
        result = sql.execute("SELECT track_id from track_genres\
                             WHERE genre_id=?\
                             LIMIT 1", (genre_id,))
        v = result.fetchone()
        if not v:
            sql.execute("DELETE FROM genres WHERE rowid=?", (genre_id,))
