from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
from pal import prediction_localisation
app = Flask(__name__)
# model = load_model('model.h5')

# model.make_predict_function()

# def predict_label(img_path):
# 	i = image.load_img(img_path, target_size=(100,100))
# 	i = image.img_to_array(i)/255.0
# 	i = i.reshape(1, 100,100,3)
# 	p = model.predict_classes(i)
# 	return dic[p[0]]


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['file']
		print(img.filename)
		img_path = "static/images/" + img.filename
		img.save(img_path)
		res_path=prediction_localisation(img_path)
		print(res_path)
		return render_template("results.html",  img_path = "image2.png")
		# p = predict_label(img_path)

	return render_template("results.html")
@app.route("/result")
def results():
		return render_template("results.html")


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)