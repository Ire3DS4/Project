from flask import Flask, render_template, request
from part1 import CentralRegistry  # the part that guides the program to the correct output


app = Flask(__name__)


@app.route('/')  # homepage
def index_page():
    r = CentralRegistry().returnregistry()
    l = CentralRegistry().returnlinks()  # to shorten links and not use registry as mentioned in part1
    return render_template('0_homepage.html', registry = r, links = l, length = 9)

@app.route('/MD')  # 2.1
def page1():
    res = CentralRegistry().link_metadata()
    return render_template('1_metadata.html', result = res)

@app.route('/Sem')  # 2.2
def page2():
    res = CentralRegistry().link_semantics()
    return render_template('2_semantics.html', result = res)

@app.route('/RecG')  # 2.3
def page3():
    res = CentralRegistry().link_genes()
    return render_template('3_geneID.html', result = res)

@app.route('/ListGUser')  # 2.4 // user input page
def user_page1():
    return render_template('4_genesentences.html')

@app.route('/ListG')  # 2.4
def page4():
    res = CentralRegistry().link_sentence_genes().listSentences(request.args.get('gene'))
    return render_template('4_genesentencesresult.html', result = res)

@app.route('/RecD')  # 2.5
def page5():
    res = CentralRegistry().link_diseases()
    return render_template('5_diseaseID.html', result = res)

@app.route('/ListDUser')  # 2.6 // user input page
def user_page2():
    return render_template('6_diseasesentences.html')

@app.route('/ListD')  # 2.6
def page6():
    res = CentralRegistry().link_sentence_diseases().listSentences(request.args.get('disease'))
    return render_template('6_diseasesentencesresult.html', result = res)

@app.route('/Top10')  # 2.7
def page7():
    res = CentralRegistry().link_top10()
    return render_template('7_top10.html', result = res)

@app.route('/GtoDUser')  # 2.8 - user input
def user_page3():
    return render_template('8_genetodiseases.html')

@app.route('/GtoD')  # 2.8
def page8():
    res = CentralRegistry().link_diseases_from_genes().associate(request.args.get('gene'))
    return render_template('8_genetodiseasesresult.html', result = res, gene = request.args.get('gene'))      

@app.route('/DtoGUser')  # 2.9 - user input
def user_page4():
    return render_template('9_diseasetogenes.html')

@app.route('/DtoG')  # 2.9
def page9():
    res = CentralRegistry().link_genes_from_diseases().associate(request.args.get('disease'))
    return render_template('9_diseasetogenesresult.html', result = res, disease = request.args.get('disease'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)