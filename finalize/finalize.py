def finalize(theta, companyIDs):
    #Calculate average topic probabilities for each company
    sentence_by_company = {}

    for ID in companyIDs :
        company_sentence = theta[companyIDs[ID]["start"]:companyIDs[ID]["end"]]
        sentence_by_company[ID] = {"list": company_sentence}

        company_sentence_sum = [0.0] * len(company_sentence[0])
        for s in company_sentence:
            for i in range(len(s)):
                company_sentence_sum[i] += float(s[i])

        sentence_by_company[ID]["topic_probs"] = [float(s/len(company_sentence)) for s in company_sentence_sum]
    
    #Calculate Similarity matrix
    from scipy.spatial import distance
    
    similarity_matrix = {}
    for c1 in sentence_by_company:
        similarity_matrix[c1] = []

        for c2 in sentence_by_company:
            probs1 = sentence_by_company[c1]["topic_probs"]
            probs2 = sentence_by_company[c2]["topic_probs"]

            similarity_matrix[c1].append(1-distance.jensenshannon(probs1, probs2))
    
    return sentence_by_company, similarity_matrix