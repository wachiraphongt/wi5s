# app.py
"""5s System"""

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    session,
)
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_manager,
    login_required,
    UserMixin,
    login_user,
    logout_user,
    current_user,
)
from markupsafe import escape

from form import LoginForm


app = Flask(__name__)

# pip install flask-sqlalchemy
# config sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)

# login manager for flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# hard coded secret key for development only
app.config["SECRET_KEY"] = "W8a9c6h2i"

# set session timeout
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

# database table
class ProjectList(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text, nullable=False)
    Owner = db.Column(db.Text, nullable=False)
    Member = db.Column(db.Text)


class LocationList(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location = db.Column(db.Text, nullable=False)


class Log(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Action = db.Column(db.Text, nullable=False)
    Person = db.Column(db.Text, nullable=False)
    Add_Date = db.Column(db.DateTime, default=datetime.today)
    Detail = db.Column(db.Text)


class User(UserMixin, db.Model):
    """Create column to store out data"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EmpID = db.Column(db.Integer, nullable=False)
    Password = db.Column(db.Text, nullable=False)
    Name = db.Column(db.Text, nullable=False)
    Role = db.Column(db.Integer, nullable=False)
    ResetPass = db.Column(db.Boolean, nullable=True, default=True)
    LastUpdated = db.Column(db.DateTime, default=datetime.today)

    def __repr__(self):
        return f"<User {self.EmpID}>"

    def __init__(self, EmpID, Password, Name, Role, ResetPass=True):
        self.EmpID = EmpID
        self.Password = Password
        self.Name = Name
        self.Role = Role
        self.ResetPass = ResetPass

    def verify_password(self, pwd):
        return check_password_hash(self.Password, pwd)


class PartRecord(db.Model):
    """ " Create this part record table to store the detail of part"""

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PartName = db.Column(db.Text, nullable=False)
    Model = db.Column(db.Text, nullable=False)
    Location = db.Column(db.Integer, db.ForeignKey("location_list.ID"), nullable=False)
    # create foreign key
    location_list = db.relationship(
        "LocationList", backref=db.backref("posts", lazy=True)
    )
    Project = db.Column(db.Integer, db.ForeignKey("project_list.ID"), nullable=False)
    # create foreign key
    project_list = db.relationship(
        "ProjectList", backref=db.backref("posts", lazy=True)
    )
    Quantity = db.Column(db.Integer, nullable=False)
    IsSpared = db.Column(db.Boolean, nullable=False)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
    # return User.query.get(1)


@app.route("/checkip")
def check_ip():
    return (
        jsonify(
            {
                "IP": request.remote_addr,
            }
        ),
        200,
    )


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index-newer.html")
    else:
        return redirect(url_for("login"))


@app.route("/projectlist/", methods=["GET", "POST"])
def project_list():

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    if request.method == "POST":

        if request.form["btn_identifier"] == "create":
            projectName = request.form["projectName"].strip()
            projectOwner = request.form["projectOwner"]

            projectCheck = ProjectList.query.filter(ProjectList.Name == projectName).first()

            if projectName == "":
                flash("Project Name can't be empty.", "danger")
            elif projectCheck != None:
                flash(
                    f"Project [ {projectCheck.Name} ] already existed. Owner : [ {projectCheck.Owner} ]",
                    "danger",
                )
            else:
                obj = ProjectList(Name=projectName, Owner=projectOwner)

                db.session.add(obj)
                db.session.commit()

                # record
                recordLog("Create_Project", f"Name:{projectName}; ")

                flash(
                    f"Project [ {projectName} ] has been created.",
                    "success",
                )

        elif request.form["btn_identifier"] == "edit":
            editProjectID = request.form["editProjectID"]
            editProjectName = request.form['editProjectName']
            editProjectMember = request.form['editProjectMember']

            print(f"{editProjectID} : {editProjectName} : {editProjectMember}")

            proj = ProjectList.query.get(editProjectID)

            proj.Name = editProjectName
            proj.Member = editProjectMember

            db.session.commit()

            recordLog("Edit_Project", f"ID:{editProjectID}; ProjectName:{editProjectName}; Member:{editProjectMember}; ")

            flash(
                    f"Project [ {editProjectName} ] has been updated.",
                    "success",
                )
            
        return redirect(url_for("project_list"))


    project_all = ProjectList.query.order_by(ProjectList.Name.asc()).all()
    project_owner = (
        ProjectList.query.filter(ProjectList.Owner == current_user.Name)
        .order_by(ProjectList.Name.asc())
        .all()
    )
    project_member = (
        ProjectList.query.filter(ProjectList.Member.like(f"%({current_user.EmpID})%"))
        .order_by(ProjectList.Name.asc())
        .all()
    )
    project_other = (
        ProjectList.query.filter(
            (ProjectList.Owner != current_user.Name)
            | (ProjectList.Member.notlike(f"({current_user.Name})"))
        )
        .order_by(ProjectList.Owner.asc(), ProjectList.Name.asc())
        .all()
    )

    return render_template(
        "project-list.html",
        project_all=project_all,
        project_owner=project_owner,
        project_member=project_member,
        project_other=project_other,
        user_all=User.query.filter(User.EmpID != 1).order_by(User.Name.asc()).all(),
    )


@app.route("/addlocation/")
def add_location():
    return ("", 204)


@app.route("/partsearch/", methods=["GET", "POST"])
@app.route("/partsearch/<location>")
def part_search(location = None):
    """search part by location"""

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    part_list = []
    part_editable = {}
    selected_location = [0, ""]

    if location != None and request.method == "GET":
        location = location.upper()
        locate = LocationList.query.filter(LocationList.Location == location).first()
        if locate != None:
            selected_location = [locate.ID, locate.Location]

            # record
            recordLog("Search", f"Location:{selected_location[1]}; ")

            # use for input location at address
            part_list = PartRecord.query.filter(
                PartRecord.Location == selected_location[0]
            ).all()

            for i in range(len(part_list)):
                
                isEditable = ProjectList.query.filter((ProjectList.ID == part_list[i].Project) & ((ProjectList.Owner == current_user.Name) | (ProjectList.Member.like(f"%({current_user.EmpID})%")))).first()

                if isEditable != None:
                    part_editable[str(part_list[i].ID)] = 1
                else:
                    if part_list[i].IsSpared:
                        part_editable[str(part_list[i].ID)] = 2
                    else:
                        part_editable[str(part_list[i].ID)] = 0

                part_list[i].Location = (
                    LocationList.query.filter(LocationList.ID == part_list[i].Location)
                    .first()
                    .Location
                )
                part_list[i].Project = (
                    ProjectList.query.filter(ProjectList.ID == part_list[i].Project)
                    .first()
                    .Name
                )

    if request.method == "POST":
        if request.form["btn_identifier"] == "search":
            location_search = request.form["location_search"]

            # check if user choose location
            if location_search != "0":

                location_number = int(location_search)
                location_name = (
                    LocationList.query.filter(LocationList.ID == location_number)
                    .first()
                    .Location
                )

                selected_location = [location_number, location_name]

                # record
                recordLog("Search", f"Location:{selected_location[1]}; ")

            # use for post
            part_list = PartRecord.query.filter(
                PartRecord.Location == selected_location[0]
            ).all()

            for i in range(len(part_list)):
                
                isEditable = ProjectList.query.filter((ProjectList.ID == part_list[i].Project) & ((ProjectList.Owner == current_user.Name) | (ProjectList.Member.like(f"%({current_user.EmpID})%")))).first()

                if isEditable != None:
                    part_editable[str(part_list[i].ID)] = 1
                else:
                    if part_list[i].IsSpared:
                        part_editable[str(part_list[i].ID)] = 2
                    else:
                        part_editable[str(part_list[i].ID)] = 0

                part_list[i].Location = (
                    LocationList.query.filter(LocationList.ID == part_list[i].Location)
                    .first()
                    .Location
                )
                part_list[i].Project = (
                    ProjectList.query.filter(ProjectList.ID == part_list[i].Project)
                    .first()
                    .Name
                )

        elif request.form["btn_identifier"] == "add":
            location_search = request.form["location_search"]

            location_number = int(location_search)
            location_name = (
                LocationList.query.filter(LocationList.ID == location_number)
                .first()
                .Location
            )

            selected_location = [location_number, location_name]

            part_list = PartRecord.query.filter(
                PartRecord.Location == selected_location[0]
            ).all()

            for part in part_list:
                part.Location = (
                    LocationList.query.filter(LocationList.ID == part.Location)
                    .first()
                    .Location
                )
                part.Project = (
                    ProjectList.query.filter(ProjectList.ID == part.Project)
                    .first()
                    .Name
                )

            # go to page part add
            return render_template(
                "partregis-newer.html",
                locationList=LocationList.query.all(),
                projectList=ProjectList.query.filter(
                    (ProjectList.Owner == current_user.Name)
                    | (ProjectList.Member.like(f"%({current_user.EmpID})%"))
                ).order_by(ProjectList.Name.asc()),
                selected_location=selected_location,
                part_list=part_list,
                partName="",
                model="",
                quantity="1",
                isSpare=False,
            )

        else:
            return ("", 204)

    return render_template(
        "partsearch.html",
        locationList=LocationList.query.all(),
        selected_location=selected_location,
        part_list=part_list,
        part_editable=part_editable,
    )


@app.route("/partregis/", methods=["GET", "POST"])
def part_register():
    """regis part to system"""

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    part_list = []
    selected_location = [0, ""]
    selected_project = 0

    partName = ""
    model = ""
    quantity = "1"
    isSpare = False
    part_list = None

    location_list = LocationList.query.all()
    # project_list = ProjectList.query.filter_by(Owner=current_user.Name).order_by(ProjectList.Name.asc())
    project_list = ProjectList.query.filter(
        (ProjectList.Owner == current_user.Name)
        | (ProjectList.Member.like(f"%({current_user.EmpID})%"))
    ).order_by(ProjectList.Name.asc())

    print(f"%{current_user.Name}%")

    # check if methid is POST
    if request.method == "POST":

        # create variable
        partName = request.form["partName"].strip()
        model = request.form["model"].strip()
        location_search = request.form["location"]  # value
        project = request.form["project"]
        quantity = request.form["quantity"].strip()
        isSpare = request.form.get("checkSpare") != None

        # check if user choose location
        if location_search != "0":

            location_number = int(location_search)
            location_name = (
                LocationList.query.filter(LocationList.ID == location_number)
                .first()
                .Location
            )

            selected_location = [location_number, location_name]

        errStatus = False

        # check use not fill all data
        all_data = [partName, model, quantity]

        if "" in all_data:
            flash(f"Invalid some data", "danger")
            errStatus = True
        elif location_search == "0" and not errStatus:
            flash(f"Please select Location", "danger")
            errStatus = True
        elif project == "0" and not errStatus:
            flash(f"Please select Project", "danger")
            errStatus = True
        elif int(quantity) <= 0 and not errStatus:
            flash(f"Quantity must be greater than 0", "danger")
            errStatus = True

        if errStatus:

            session["selected_project"] = project
            session["selected_location"] = selected_location[0]

            return redirect(url_for("part_register"))

        obj = PartRecord(
            PartName=partName,
            Model=model,
            Location=selected_location[0],
            Project=project,
            Quantity=quantity,
            IsSpared=isSpare,
        )

        db.session.add(obj)
        db.session.commit()

        projectName = ProjectList.query.filter(ProjectList.ID == project).first().Name

        recordLog(
            "Add_Part",
            f"PartName:{partName}; Model:{model}; Location:{selected_location[1]}; Project:{projectName}; Qty:{quantity}; IsSpared:{isSpare}; ",
        )

        flash(f"Add Part Successfully", "success")

        session["selected_project"] = project
        session["selected_location"] = selected_location[0]

        return redirect(url_for("part_register"))

    if "selected_project" in session:
        selected_project = escape(session["selected_project"])
        session.pop("selected_project", None)

    if "selected_location" in session:
        selected_location[0] = int(escape(session["selected_location"]))
        session.pop("selected_location", None)

    # check if user choose location
    if selected_location[0] != 0:
        location_name = (
            LocationList.query.filter(LocationList.ID == selected_location[0])
            .first()
            .Location
        )
        selected_location[1] = location_name

        part_list = PartRecord.query.filter(
            PartRecord.Location == selected_location[0]
        ).all()

        for part in part_list:
            part.Location = (
                LocationList.query.filter(LocationList.ID == part.Location)
                .first()
                .Location
            )
            part.Project = (
                ProjectList.query.filter(ProjectList.ID == part.Project).first().Name
            )

    return render_template(
        "partregis-newer.html",
        locationList=location_list,
        projectList=project_list,
        selected_location=selected_location,
        selected_project=selected_project,
        part_list=part_list,
        partName=partName,
        model=model,
        quantity=quantity,
        isSpare=isSpare,
    )


@app.route("/partuse/")
def part_use():
    return redirect(url_for("home"))


@app.route("/partcheck/")
def part_check():
    return redirect(url_for("home"))


@app.route("/sign-up/", methods=["GET", "POST"])
@login_required
def sign_up():
    """sign up user account"""

    empID = ""
    empName = ""
    empPass = ""
    empRole = 1

    # check if method is POST
    if request.method == "POST":

        # create variable
        empID = request.form["EmpID"].strip()
        empName = request.form["EmpName"].strip()
        empPass = request.form["Password"].strip()
        empRole = request.form["Role"].strip()

        # show details
        print(f"id   : {empID}\nname : {empName}\npass : {empPass}\nrole : {empRole}")

        # check valid
        if empID == "" or empName == "" or empPass == "" or empRole == "":

            # show error
            flash(f"Invalid some data", "danger")

            return render_template(
                "sign-up.html",
                empID=empID,
                empName=empName,
                empPass=empPass,
                empRole=empRole,
            )

        if int(empRole) == 99:
            empRole = 99
        else:
            empRole = 1

        testExist = User.query.filter(User.EmpID == empID).first()

        if testExist:
            flash(f"'{empID}' already existed as '{testExist.Name}'", "danger")
        else:
            # hash password
            empPass = generate_password_hash(empPass, method="sha256")

            # create an objects then pass variables into user class
            obj = User(EmpID=empID, Password=empPass, Name=empName, Role=empRole)

            db.session.add(obj)
            db.session.commit()

            flash(f"Successful Sign up : {empName}", "success")

            # reset all parameter
            empID = ""
            empName = ""
            empPass = ""
            empRole = 1

    return render_template(
        "sign-up.html",
        empID=empID,
        empName=empName,
        empPass=empPass,
        empRole=empRole,
    )


@app.route("/reset-pwd/")
def reset_pwd():
    """page to reset password"""

    return render_template("reset-pwd.html")


@app.route("/logout/")
@login_required
def logout():
    if current_user.is_authenticated:
        # record
        recordLog("Logout", f"Name:{current_user.Name}; ")
        logout_user()
    return redirect(url_for("login"))


@app.route("/login/", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    # Create an object called "form" to use LoginForm class
    form = LoginForm()

    EmpID = form.EmpID.data
    EmpPass = form.Password.data

    # Validate a form submitted by user
    if form.validate_on_submit():
        # Query a user's username from the database
        emp = User.query.filter_by(EmpID=EmpID).first()

        # Check and compare a user's password
        # in a database, if True, log a user in
        if emp and emp.verify_password(EmpPass):
            # Log a user in after completing verifying a password
            # then flash a message "Successful Login"
            login_user(emp)
            session.permanent = True

            flash(f"Successful Login. Hi, {current_user.Name} !", "success")

            # record
            recordLog("Login", f"Name:{current_user.Name}; ")

            # redirect to homepage
            return redirect(url_for("home"))
        else:
            # show flash message "invalid login" if login gets False
            flash("Invalid Login", "danger")

    else:
        # you can print or return something such as an error message
        # In this case, do nothing. But you can do it later
        pass

    return render_template("login.html", form=form, noNav=True)


def recordLog(action, detail):
    obj = Log(
        Action=action,
        Person=current_user.EmpID,
        Detail=detail,
    )

    db.session.add(obj)
    db.session.commit()

    return

@app.route('/log/')
def show_log():
    return render_template(
        'show-log.html',
        logs = Log.query.order_by(Log.ID.desc()).limit(100)
    )


if __name__ == "__main__":
    # app.run(debug=True, host="172.31.194.201", port=5555)
    # app.run(debug=True, host="192.168.1.46", port=5500)
    app.run(debug=True, host="192.168.1.55", port=5555)
    # app.run(debug=True)
