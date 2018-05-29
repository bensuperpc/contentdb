# Content DB
# Copyright (C) 2018  rubenwardy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from flask import *
from flask_user import *
from app import app
from app.models import *
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from app.utils import rank_required

@app.route("/tags/")
@rank_required(UserRank.MODERATOR)
def tag_list_page():
	return render_template("tags/list.html", tags=Tag.query.order_by(db.asc(Tag.title)).all())

class TagForm(FlaskForm):
	title	 = StringField("Title", [InputRequired(), Length(3,100)])
	name     = StringField("Name", [Optional(), Length(1, 20), Regexp("^[a-z0-9_]", 0, "Lower case letters (a-z), digits (0-9), and underscores (_) only")])
	submit   = SubmitField("Save")

@app.route("/tags/new/", methods=["GET", "POST"])
@app.route("/tags/<name>/edit/", methods=["GET", "POST"])
@rank_required(UserRank.MODERATOR)
def createedit_tag_page(name=None):
	tag = None
	if name is not None:
		tag = Tag.query.filter_by(name=name).first()
		if tag is None:
			abort(404)

	form = TagForm(formdata=request.form, obj=tag)
	if request.method == "POST" and form.validate():
		if tag is None:
			tag = Tag(form.title.data)
			db.session.add(tag)
		else:
			form.populate_obj(tag)
		db.session.commit()
		return redirect(url_for("createedit_tag_page", name=tag.name))

	return render_template("tags/edit.html", tag=tag, form=form)
