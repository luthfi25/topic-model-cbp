import collections
import operator

def prepare_background(topics, definitions, placeHolderText):
    print("Begin preparing background knowledge {}...".format(placeHolderText))
    definitions = [d.split(" ") for d in definitions]  

    result = []
    for i in range(len(topics)):
        definition = definitions[i]
        topic = topics[i]
        word_occurence = {}

        for word in definition:
            word_occurence[word] = definition.count(word)
    
        sorted_word_occurence = sorted(word_occurence.items(), key=operator.itemgetter(1), reverse=True)
        sorted_word_occurence = collections.OrderedDict(sorted_word_occurence)
        result.append(topic + ' ' + ' '.join(['%s %s' % (key, value) for (key,value) in sorted_word_occurence.items()]))
    
    print("Finish preparing background knowledge {}...".format(placeHolderText))
    return result