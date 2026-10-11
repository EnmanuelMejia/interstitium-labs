#!/usr/bin/env python3
"""Inject animated AI algorithm visualizations (il-algo-viz) into courses + topics.
Idempotent: skips notes/sections already present."""
import json, os, re, sys

BASE = os.path.expanduser('~/workspace/apex-audit/docs')
COURSES = os.path.join(BASE, 'university/data/courses')
MARK = '[AAV]'

TITLES = {
 'linear-regression':'Linear Regression','logistic-regression':'Logistic Regression',
 'decision-tree':'Decision Tree','random-forest':'Random Forest','svm':'Support Vector Machine',
 'knn':'k-Nearest Neighbors','naive-bayes':'Naive Bayes','gradient-boosting':'Gradient Boosting',
 'adaboost':'AdaBoost','xgboost':'XGBoost','k-means':'k-Means Clustering',
 'hierarchical-clustering':'Hierarchical Clustering','dbscan':'DBSCAN','pca':'Principal Component Analysis',
 'tsne':'t-SNE','actor-critic':'Actor-Critic','gaussian-mixture':'Gaussian Mixture Model',
 'policy-gradient':'Policy Gradient','sarsa':'SARSA','q-learning':'Q-Learning','transformer':'Transformer',
 'lstm':'LSTM','rnn':'Recurrent Neural Network','cnn':'Convolutional Neural Network',
 'ann':'Artificial Neural Network','genetic-algorithms':'Genetic Algorithms',
 'markov-decision-process':'Markov Decision Process','isolation-forest':'Isolation Forest',
 'autoencoders':'Autoencoders',
}

# course file -> {module_id: [algo slugs]}
PLAN = {
 'il-16-machine-learning-ai-engineering.json': {
  'IL-16-PM-STATS': ['linear-regression','logistic-regression'],
  'IL-16-PM-LINALG': ['pca','svm'],
  'IL-16-PM-DISCRETE': ['decision-tree','markov-decision-process'],
  'advanced-ml--ensemble-methods-practice': ['random-forest','gradient-boosting','adaboost','xgboost'],
  'advanced-ml--probabilistic-ml': ['naive-bayes','gaussian-mixture'],
  'advanced-ml--deep-architectures-practice': ['ann','cnn','autoencoders'],
  'advanced-ml--optimization-advanced': ['genetic-algorithms','q-learning','sarsa','policy-gradient','actor-critic'],
  'advanced-nlp-practice--sequence-models-practice': ['rnn','lstm'],
  'advanced-genai--transformer-arch-practice': ['transformer'],
  'ml-in-practice--model-evaluation-practice': ['knn','isolation-forest'],
  'python-for-ml--visualization-practice': ['tsne','k-means','dbscan','hierarchical-clustering'],
 },
 'il-12-ai-engineering.json': {
  'aieng-machine-learning--supervised-learning': ['linear-regression','logistic-regression','decision-tree','random-forest','svm','knn','naive-bayes','gradient-boosting','adaboost','xgboost'],
  'aieng-machine-learning--unsupervised-learning': ['k-means','hierarchical-clustering','dbscan','pca','tsne','gaussian-mixture','isolation-forest'],
  'aieng-machine-learning--reinforcement-intro': ['markov-decision-process','q-learning','sarsa','policy-gradient','actor-critic'],
  'aieng-deep-learning--neural-foundations': ['ann'],
  'aieng-deep-learning--cnns': ['cnn'],
  'aieng-deep-learning--sequence-models': ['rnn','lstm'],
  'aieng-generative-ai--transformers-attention': ['transformer'],
  'aieng-generative-ai--gans-vaes': ['autoencoders'],
  'aieng-deep-learning--backprop-optimization': ['genetic-algorithms'],
 },
 'il-17-agentic-ai-engineering.json': {
  'agentic-ai-foundations--agent-loops': ['markov-decision-process','q-learning','sarsa','policy-gradient','actor-critic'],
  'agentic-ai-for-iv--llm-depth-iv': ['transformer','rnn','lstm'],
  'IL-17-PM-STATS': ['naive-bayes'],
 },
 'il-26-data-analyst-certification-senior-mastery.json': {
  'IL26-M31': ['linear-regression'],
  'IL26-M10': ['logistic-regression','naive-bayes'],
  'IL26-M33': ['pca','svm'],
  'IL26-M15': ['k-means','hierarchical-clustering','dbscan','tsne'],
  'IL26-M09': ['decision-tree','random-forest','knn','gradient-boosting','isolation-forest'],
 },
}

def fig(slug):
    return '<figure class="aav" data-algo="%s"></figure>' % slug

def inject_courses():
    total = 0
    for fname, modmap in PLAN.items():
        path = os.path.join(COURSES, fname)
        d = json.load(open(path))
        changed = False
        mods = {m['id']: m for m in d['modules']}
        for mid, slugs in modmap.items():
            m = mods.get(mid)
            if not m:
                print('  WARN module not found: %s in %s' % (mid, fname)); continue
            notes = m.setdefault('notes', [])
            for slug in slugs:
                title = '%s Watch it work: %s' % (MARK, TITLES[slug])
                if any(n.get('title') == title for n in notes): continue
                notes.append({
                    'title': title,
                    'body': 'Animated inline visualization — watch the algorithm work, step by step.\n\n' + fig(slug)
                })
                changed = True; total += 1
        if changed:
            tmp = path + '.aavtmp'
            with open(tmp, 'w') as f: json.dump(d, f, indent=2, ensure_ascii=False)
            json.load(open(tmp))  # validate
            os.replace(tmp, path)
            print('  %s: injected' % fname)
    print('course notes injected: %d' % total)

CSS_LINK = '<link rel="stylesheet" href="/assets/il-algo-viz.css"/>'
JS_SCRIPT = '<script src="/assets/il-algo-viz.js" defer></script>'

def ensure_head_assets(path):
    src = open(path).read()
    orig = src
    if 'il-algo-viz.css' not in src:
        src = src.replace('</head>', '  ' + CSS_LINK + '\n</head>', 1)
    if 'il-algo-viz.js' not in src:
        src = src.replace('</body>', '  ' + JS_SCRIPT + '\n</body>', 1)
    if src != orig:
        open(path, 'w').write(src)
        print('  head assets added: %s' % path)
    return src != orig

TOPIC_SECTIONS = {
 'ai-ml': (['linear-regression','logistic-regression','decision-tree','random-forest','svm','knn','naive-bayes','gradient-boosting','adaboost','xgboost','k-means','hierarchical-clustering','dbscan','pca','tsne','actor-critic','gaussian-mixture','policy-gradient','sarsa','q-learning','transformer','lstm','rnn','cnn','ann','genetic-algorithms','markov-decision-process','isolation-forest','autoencoders'],
           'How the algorithms actually work',
           'Twenty-nine core algorithms, each animated inline. Watch decision boundaries form, clusters merge, gradients flow, and attention fire — the mechanics, not just the math.'),
 'data-eng': (['linear-regression','logistic-regression','decision-tree','random-forest','k-means','pca','naive-bayes','isolation-forest'],
           'Algorithms in the data pipeline',
           'The workhorse algorithms behind analytics and feature engineering, animated inline.'),
 'math': (['linear-regression','logistic-regression','pca','naive-bayes','markov-decision-process'],
           'The mathematics, animated',
           'Core mathematical machinery behind machine learning, animated inline.'),
}

def inject_topics():
    for slug, (algos, heading, lede) in TOPIC_SECTIONS.items():
        path = os.path.join(BASE, 'topics', slug, 'index.html')
        src = open(path).read()
        if 'data-aav-topicsec' in src:
            print('  topics/%s: section already present' % slug); 
        else:
            figs = '\n'.join('      ' + fig(a) for a in algos)
            sec = ('\n<section class="aav-sec" data-aav-topicsec>\n'
                   '  <h3>%s</h3>\n  <p class="aav-lede">%s</p>\n'
                   '  <div class="aav-grid">\n%s\n  </div>\n</section>\n') % (heading, lede, figs)
            src = src.replace('</main>', sec + '</main>', 1)
            open(path, 'w').write(src)
            print('  topics/%s: section injected (%d algos)' % (slug, len(algos)))
        ensure_head_assets(path)

if __name__ == '__main__':
    print('== courses =='); inject_courses()
    print('== course.html =='); ensure_head_assets(os.path.join(BASE, 'university/course.html'))
    print('== topics =='); inject_topics()
    print('done')
