asicBilat = """  (scope asic.transaction-reporting/bilateral-party
            (include
                :citation "/document/F2015C00262/annotation/2031"
                (any :party {the-party is asic-reporting/reporting-entity})))"""
emirBilat = """  (scope esma-gs.listed-derivative-valuation-reporting/bilateral-party
                    (include
                    (any
                        :party
                        {the-party is emir/financial-counterparty}
                        {the-party is-not emir/exempted-counterparty}))
                    (include
                    (any
                        :party
                        {the-party is emir/non-financial-counterparty-plus}
                        {the-party is-not emir/exempted-counterparty}))
                    (exclude
                    (all :party {the-party is emir/exempt-intragroup-affiliates})
                    (any
                        :party
                        {the-party is emir/non-financial-counterparty}
                        {the-party is-not emir/third-country-entity}
                        {the-party is-not emir/child-of-financial-counterparty-parent})))"""
mifirBilat = """   (scope esma.mifir-transaction-reporting/bilateral-party
    (include
      :citation "MiFID-II art. 27(6)"
      (any
        :party
        {the-party is mifid/investment-firm}
        (in :NotApplicable {mifid/exemptions of the-party}))))"""
oscBilat= """ (scope osc.transaction-reporting/bilateral-party
    (include
      :citation "OSC Rule 91-507 sec. 25(1)"
      (any
        :party
        {the-party is osc.transaction-reporting/local-counterparty}))
    (exclude
      :citation "OSC Rule 91-507 sec. 41"
      (all
        :party
        {the-party is osc.transaction-reporting/exempted-counterparty}))
    (exclude
      :citation "OSC Rule 91-507 sec. 41.1"
      (all
        :party
        {the-party is common/affiliate}
        {the-party is-not osc.transaction-reporting/derivative-dealer}
        {the-party is-not osc.transaction-reporting/clearing-agency}
        {the-party is-not osc.transaction-reporting/affiliate-of-derivative-dealer}
        {the-party is-not osc.transaction-reporting/affiliate-of-clearing-agency})))"""
sfcBilat = """  (scope sfc-gs.transaction-reporting/bilateral-party
    (include
      :citation "CAP571AL Part 1 Sec 5"
      (any
        :party
        {the-party is sfc-gs.transaction-reporting/recognized-clearing-house}))
    (include
      :citation "CAP571AL Part 1 Sec 5"
      (any :party {the-party is sfc-gs.transaction-reporting/ATS-CCP}))
    (include
      :citation ["CAP571AL Part 2 Sec 10" "CAP571AL Part 1 Sec 3(2)"]
      (any
        :party
        {the-party is sfc/licensed-corporation}
        {the-party is-not sfc-gs.transaction-reporting/phase-2-exempt-person}))
    (include
      :citation ["CAP571AL Part 2 Sec 11" "CAP571AL Part 1 Sec 3(2)"]
      (any
        :party
        {the-party is sfc/authorized-financial-institution}
        {the-party is-not sfc-gs.transaction-reporting/phase-2-exempt-person}))
    (include
      :citation ["CAP571AL Part 2 Sec 13" "CAP571AL Part 1 Sec 3(2)"]
      (any
        :party
        {the-party is sfc/approved-money-broker}
        {the-party is-not sfc-gs.transaction-reporting/phase-2-exempt-person}))
    (include
      :citation ["CAP571AL Part 4 Sec 32" "CAP571AL Part 1 Sec 3(2)"]
      (any
        :party
        {the-party is sfc-gs.transaction-reporting/specified-subsidiary}
        {the-party is-not sfc-gs.transaction-reporting/phase-2-exempt-person})))"""      


emirProd = """  (scope product
                    (include
                    {product is esma-gs.listed-derivative-valuation-reporting/exchange-traded-derivative}))"""
asicProd = """  (scope product
                (exclude
                :citation "/document/C2017C00129-v4/annotation/2038"
                (= {isda/asset-class of product} :Commodity)
                (= {isda/settlement-type of product} :Physical))
                (exclude
                :citation "/document/F2015C00262/annotation/2019"
                (= {isda/asset-class of product} :Commodity)
                (= {isda/sub-product of product} :Elec))
                (exclude
                :citation "/document/C2017C00129-v4/annotation/2039"
                (= {isda/asset-class of product} :ForeignExchange)
                (in {isda/base-product of product} [:Spot
                                                    :Forward])
                {product is-not common/fx-swap-near-leg}
                {product is-not common/fx-swap-far-leg}
                (<=
                    {fpml/fx-settlement-offset-after-valuation of product}
                    (tenor 2 :d)))
                (exclude
                :citation "/document/F2018C00687/annotation/2033"
                (= {isda/asset-class of product} :ForeignExchange)
                (in {isda/base-product of product} [:Spot
                                                    :Forward])
                {product is-not common/fx-swap-near-leg}
                {product is-not common/fx-swap-far-leg}
                (>
                    {fpml/fx-settlement-offset-after-valuation of product}
                    (tenor 2 :d))
                (<=
                    {fpml/fx-settlement-offset-after-valuation of product}
                    (tenor 7 :d))
                {transaction is common/facilitate-security-settlement}))"""


d={}
def bilatScope(lis, length, finalList):
    aList=["Does transaction satisfy bilateral party scope?"]
    i = 2
    while i < length:
        if ("include" in lis[i]) or ("exclude" in lis[i]):
            for j in range(i, length):
                i = j
                if "any" in lis[j]:
                    sentence = "Does any party satisfy the condition(s)?"
                    aList.append(sentence)
                elif "all" in lis[j]:
                    aList.append("Do all parties satisfy the condition(s)?")
                for k in range(j, length):
                    if lis[k]== "is" or lis[k] == "is-not":
                        entity = lis[k+1].split("/")[1]
                        entity = entity.replace(")", "")
                        entity = entity.replace("}", "")
                        entity = entity.replace("-", " ")
                        sentence = "Is the party a(n) "+entity+"?"
                        if lis[k] == "is-not":
                            sentence = "Is the party not a(n) "+entity+"?"
                        aList.append(sentence)
                        i = k+1
                        j = k+1
                        if ("))" in lis[k+1]) or ("all" in lis[k+2]) or ("any" in lis[k+2]):
                            break
            i = i+1
        i = i+1
    return aList
            

def prodScope(lis, length):
    aList=["Does transaction satisfy product scope?"]
    i = 2
    while i < length:
        if ("include" in lis[i]) or ("exclude" in lis[i]):
            for j in range(i, length):
                i = j
                if lis[j] == "is" or lis[j] == "is-not":
                    entity = lis[j+1].split("/")[1]
                    entity = entity.replace(")", "")
                    entity = entity.replace("}", "")
                    entity = entity.replace("-", " ")
                    sentence = "Is the product a(n) "+entity+"?"
                    if lis[j] == "is-not":
                        sentence = "Is the product not a(n) "+entity+"?"
                    aList.append(sentence)
                    i = j+1

                
                






def process(scope, d):
    lis = ' '.join(scope.split(" "))
    lis2 = lis.split()
    if "bilateral-party" in lis2[1]:
        result = bilatScope(lis2, len(lis2))
        d["bilateral-scope"] = result
    elif "product" in lis2[1]:
        result = prodScope(lis2, len(lis2))


 


process(asicBilat)
process(emirBilat)
process(mifirBilat)
process(oscBilat)
process(sfcBilat)
