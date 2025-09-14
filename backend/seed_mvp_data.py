#!/usr/bin/env python3
"""
Seed MVP Legal Database with Sample Data
Creates sample case law, statutes, and precedents for testing
"""

import json
import logging
import os
import sys
from datetime import datetime, date

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.sqlite_legal_manager import LegalDataManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_case_law(db_manager):
    """Seed case law database with sample cases"""
    sample_cases = [
        {
            'case_law_id': 'case_001',
            'case_name': 'Miranda v. Arizona',
            'citation': '384 U.S. 436 (1966)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1966-06-13',
            'judge_name': 'Chief Justice Earl Warren',
            'legal_issues': json.dumps(['Criminal Procedure', 'Fifth Amendment', 'Self-Incrimination', 'Right to Counsel']),
            'holding': 'The prosecution may not use statements stemming from custodial interrogation of defendants unless it demonstrates the use of procedural safeguards effective to secure the privilege against self-incrimination.',
            'key_facts': 'Defendant was arrested and interrogated by police without being informed of his constitutional rights.',
            'legal_reasoning': 'The Court held that the Fifth Amendment privilege against self-incrimination requires that law enforcement officials advise suspects of their rights before interrogation.',
            'precedent_type': 'binding',
            'citation_count': 15000,
            'relevance_keywords': json.dumps(['Miranda rights', 'custodial interrogation', 'Fifth Amendment', 'criminal procedure']),
            'practice_areas': json.dumps(['Criminal Law', 'Constitutional Law']),
            'summary': 'Landmark case establishing Miranda rights for criminal suspects in police custody.'
        },
        {
            'case_law_id': 'case_002',
            'case_name': 'Brown v. Board of Education',
            'citation': '347 U.S. 483 (1954)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1954-05-17',
            'judge_name': 'Chief Justice Earl Warren',
            'legal_issues': json.dumps(['Equal Protection', 'Fourteenth Amendment', 'Education', 'Segregation']),
            'holding': 'Separate educational facilities are inherently unequal and violate the Equal Protection Clause of the Fourteenth Amendment.',
            'key_facts': 'African American children were denied admission to public schools attended by white children under laws requiring racial segregation.',
            'legal_reasoning': 'The Court found that segregation in public education creates a feeling of inferiority that affects children\'s motivation to learn and has a detrimental effect on their educational development.',
            'precedent_type': 'binding',
            'citation_count': 12000,
            'relevance_keywords': json.dumps(['equal protection', 'segregation', 'education', 'Fourteenth Amendment']),
            'practice_areas': json.dumps(['Constitutional Law', 'Civil Rights', 'Education Law']),
            'summary': 'Landmark case that declared racial segregation in public schools unconstitutional.'
        },
        {
            'case_law_id': 'case_003',
            'case_name': 'Roe v. Wade',
            'citation': '410 U.S. 113 (1973)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1973-01-22',
            'judge_name': 'Justice Harry Blackmun',
            'legal_issues': json.dumps(['Privacy', 'Due Process', 'Fourteenth Amendment', 'Abortion Rights']),
            'holding': 'The Constitution protects a woman\'s right to choose to have an abortion, subject to certain limitations.',
            'key_facts': 'Texas law made it a crime to perform an abortion except to save the life of the mother.',
            'legal_reasoning': 'The Court found that the right to privacy, though not explicitly mentioned in the Constitution, is fundamental and includes a woman\'s right to choose abortion.',
            'precedent_type': 'binding',
            'citation_count': 8000,
            'relevance_keywords': json.dumps(['privacy', 'abortion', 'reproductive rights', 'due process']),
            'practice_areas': json.dumps(['Constitutional Law', 'Health Law', 'Civil Rights']),
            'summary': 'Landmark case establishing constitutional right to abortion under the Due Process Clause.'
        },
        {
            'case_law_id': 'case_004',
            'case_name': 'Marbury v. Madison',
            'citation': '5 U.S. 137 (1803)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1803-02-24',
            'judge_name': 'Chief Justice John Marshall',
            'legal_issues': json.dumps(['Judicial Review', 'Separation of Powers', 'Constitutional Law']),
            'holding': 'The Supreme Court has the authority to declare acts of Congress unconstitutional through the power of judicial review.',
            'key_facts': 'William Marbury sued Secretary of State James Madison for failing to deliver his commission as a justice of the peace.',
            'legal_reasoning': 'The Court established that it is the duty of the judicial department to say what the law is, and that laws repugnant to the Constitution are void.',
            'precedent_type': 'binding',
            'citation_count': 10000,
            'relevance_keywords': json.dumps(['judicial review', 'separation of powers', 'constitutional law', 'supreme court']),
            'practice_areas': json.dumps(['Constitutional Law', 'Administrative Law']),
            'summary': 'Landmark case establishing the principle of judicial review.'
        },
        {
            'case_law_id': 'case_005',
            'case_name': 'Gideon v. Wainwright',
            'citation': '372 U.S. 335 (1963)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1963-03-18',
            'judge_name': 'Justice Hugo Black',
            'legal_issues': json.dumps(['Right to Counsel', 'Sixth Amendment', 'Due Process', 'Criminal Procedure']),
            'holding': 'The Sixth Amendment right to counsel applies to state criminal proceedings through the Due Process Clause of the Fourteenth Amendment.',
            'key_facts': 'Clarence Gideon was charged with breaking and entering but was denied counsel because Florida law only provided counsel for capital cases.',
            'legal_reasoning': 'The Court held that the right to counsel is fundamental and essential to a fair trial, and applies to all criminal prosecutions.',
            'precedent_type': 'binding',
            'citation_count': 7000,
            'relevance_keywords': json.dumps(['right to counsel', 'Sixth Amendment', 'criminal procedure', 'fair trial']),
            'practice_areas': json.dumps(['Criminal Law', 'Constitutional Law']),
            'summary': 'Landmark case establishing the right to counsel in state criminal proceedings.'
        },
        {
            'case_law_id': 'case_006',
            'case_name': 'Mapp v. Ohio',
            'citation': '367 U.S. 643 (1961)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1961-06-19',
            'judge_name': 'Justice Tom Clark',
            'legal_issues': json.dumps(['Fourth Amendment', 'Search and Seizure', 'Exclusionary Rule', 'Due Process']),
            'holding': 'Evidence obtained in violation of the Fourth Amendment is inadmissible in state criminal proceedings.',
            'key_facts': 'Police entered Dollree Mapp\'s home without a warrant and found obscene materials, which were used to convict her.',
            'legal_reasoning': 'The Court held that the exclusionary rule applies to the states through the Fourteenth Amendment to ensure Fourth Amendment rights are protected.',
            'precedent_type': 'binding',
            'citation_count': 6000,
            'relevance_keywords': json.dumps(['Fourth Amendment', 'search and seizure', 'exclusionary rule', 'due process']),
            'practice_areas': json.dumps(['Criminal Law', 'Constitutional Law']),
            'summary': 'Landmark case extending the exclusionary rule to state criminal proceedings.'
        },
        {
            'case_law_id': 'case_007',
            'case_name': 'Terry v. Ohio',
            'citation': '392 U.S. 1 (1968)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1968-06-10',
            'judge_name': 'Chief Justice Earl Warren',
            'legal_issues': json.dumps(['Fourth Amendment', 'Stop and Frisk', 'Reasonable Suspicion', 'Search and Seizure']),
            'holding': 'Police may stop and frisk a suspect without probable cause if they have reasonable suspicion of criminal activity.',
            'key_facts': 'Police officer observed suspicious behavior and conducted a pat-down search that revealed a weapon.',
            'legal_reasoning': 'The Court balanced the need for effective law enforcement with individual privacy rights, establishing the reasonable suspicion standard.',
            'precedent_type': 'binding',
            'citation_count': 5000,
            'relevance_keywords': json.dumps(['Fourth Amendment', 'stop and frisk', 'reasonable suspicion', 'police powers']),
            'practice_areas': json.dumps(['Criminal Law', 'Constitutional Law']),
            'summary': 'Landmark case establishing the stop and frisk doctrine under the Fourth Amendment.'
        },
        {
            'case_law_id': 'case_008',
            'case_name': 'New York Times v. Sullivan',
            'citation': '376 U.S. 254 (1964)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1964-03-09',
            'judge_name': 'Justice William Brennan',
            'legal_issues': json.dumps(['First Amendment', 'Defamation', 'Freedom of Press', 'Actual Malice']),
            'holding': 'Public officials cannot recover damages for defamation unless they prove actual malice.',
            'key_facts': 'The New York Times published an advertisement critical of police actions in Alabama, leading to a defamation lawsuit.',
            'legal_reasoning': 'The Court held that the First Amendment requires a higher standard for defamation claims by public officials to protect freedom of speech and press.',
            'precedent_type': 'binding',
            'citation_count': 4000,
            'relevance_keywords': json.dumps(['First Amendment', 'defamation', 'freedom of press', 'actual malice']),
            'practice_areas': json.dumps(['Constitutional Law', 'Media Law', 'Civil Rights']),
            'summary': 'Landmark case establishing the actual malice standard for defamation of public officials.'
        },
        {
            'case_law_id': 'case_009',
            'case_name': 'Brandenburg v. Ohio',
            'citation': '395 U.S. 444 (1969)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1969-06-09',
            'judge_name': 'Per Curiam',
            'legal_issues': json.dumps(['First Amendment', 'Free Speech', 'Incitement', 'Clear and Present Danger']),
            'holding': 'Speech can only be prohibited if it is directed to inciting imminent lawless action and is likely to produce such action.',
            'key_facts': 'Brandenburg, a KKK leader, was convicted under Ohio\'s criminal syndicalism law for advocating violence.',
            'legal_reasoning': 'The Court held that abstract advocacy of violence is protected speech unless it incites imminent lawless action.',
            'precedent_type': 'binding',
            'citation_count': 3000,
            'relevance_keywords': json.dumps(['First Amendment', 'free speech', 'incitement', 'clear and present danger']),
            'practice_areas': json.dumps(['Constitutional Law', 'Civil Rights']),
            'summary': 'Landmark case establishing the Brandenburg test for incitement speech under the First Amendment.'
        },
        {
            'case_law_id': 'case_010',
            'case_name': 'Loving v. Virginia',
            'citation': '388 U.S. 1 (1967)',
            'court': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'decision_date': '1967-06-12',
            'judge_name': 'Chief Justice Earl Warren',
            'legal_issues': json.dumps(['Equal Protection', 'Due Process', 'Fourteenth Amendment', 'Marriage Rights']),
            'holding': 'Laws prohibiting interracial marriage violate both the Equal Protection and Due Process Clauses of the Fourteenth Amendment.',
            'key_facts': 'Virginia couple was convicted under state law prohibiting interracial marriage.',
            'legal_reasoning': 'The Court held that marriage is a fundamental right and racial classifications are subject to strict scrutiny.',
            'precedent_type': 'binding',
            'citation_count': 2500,
            'relevance_keywords': json.dumps(['equal protection', 'due process', 'marriage rights', 'Fourteenth Amendment']),
            'practice_areas': json.dumps(['Constitutional Law', 'Civil Rights', 'Family Law']),
            'summary': 'Landmark case striking down laws prohibiting interracial marriage.'
        }
    ]
    
    for case in sample_cases:
        try:
            db_manager.conn.execute('''
                INSERT OR REPLACE INTO case_law 
                (case_law_id, case_name, citation, court, jurisdiction, decision_date, judge_name,
                 legal_issues, holding, key_facts, legal_reasoning, precedent_type, citation_count,
                 relevance_keywords, practice_areas, summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                case['case_law_id'], case['case_name'], case['citation'], case['court'],
                case['jurisdiction'], case['decision_date'], case['judge_name'],
                case['legal_issues'], case['holding'], case['key_facts'], case['legal_reasoning'],
                case['precedent_type'], case['citation_count'], case['relevance_keywords'],
                case['practice_areas'], case['summary']
            ))
            logger.info(f"Added case law: {case['case_name']}")
        except Exception as e:
            logger.error(f"Failed to add case law {case['case_name']}: {str(e)}")
    
    db_manager.conn.commit()

def seed_statutes(db_manager):
    """Seed statutes database with sample laws"""
    sample_statutes = [
        {
            'statute_id': 'stat_001',
            'title': 'Civil Rights Act of 1964',
            'citation': '42 U.S.C. § 2000e',
            'jurisdiction': 'federal',
            'chapter': '42',
            'section': '2000e',
            'effective_date': '1964-07-02',
            'statute_text': 'It shall be an unlawful employment practice for an employer to fail or refuse to hire or to discharge any individual, or otherwise to discriminate against any individual with respect to his compensation, terms, conditions, or privileges of employment, because of such individual\'s race, color, religion, sex, or national origin.',
            'summary': 'Prohibits employment discrimination based on race, color, religion, sex, or national origin.',
            'keywords': json.dumps(['employment discrimination', 'civil rights', 'equal opportunity', 'workplace']),
            'practice_areas': json.dumps(['Employment Law', 'Civil Rights']),
            'related_regulations': json.dumps(['29 C.F.R. § 1604', '29 C.F.R. § 1606'])
        },
        {
            'statute_id': 'stat_002',
            'title': 'Americans with Disabilities Act',
            'citation': '42 U.S.C. § 12101',
            'jurisdiction': 'federal',
            'chapter': '42',
            'section': '12101',
            'effective_date': '1990-07-26',
            'statute_text': 'The purposes of this Act are to provide a clear and comprehensive national mandate for the elimination of discrimination against individuals with disabilities and to provide clear, strong, consistent, enforceable standards addressing discrimination against individuals with disabilities.',
            'summary': 'Prohibits discrimination against individuals with disabilities in employment, public accommodations, and other areas.',
            'keywords': json.dumps(['disability discrimination', 'accessibility', 'reasonable accommodation', 'ADA']),
            'practice_areas': json.dumps(['Disability Law', 'Employment Law', 'Civil Rights']),
            'related_regulations': json.dumps(['28 C.F.R. § 35', '29 C.F.R. § 1630'])
        },
        {
            'statute_id': 'stat_003',
            'title': 'Family and Medical Leave Act',
            'citation': '29 U.S.C. § 2601',
            'jurisdiction': 'federal',
            'chapter': '29',
            'section': '2601',
            'effective_date': '1993-02-05',
            'statute_text': 'The purposes of this Act are to balance the demands of the workplace with the needs of families, to promote the stability and economic security of families, and to promote national interests in preserving family integrity.',
            'summary': 'Provides eligible employees with up to 12 weeks of unpaid, job-protected leave for specified family and medical reasons.',
            'keywords': json.dumps(['family leave', 'medical leave', 'FMLA', 'employee rights']),
            'practice_areas': json.dumps(['Employment Law', 'Labor Law']),
            'related_regulations': json.dumps(['29 C.F.R. § 825'])
        },
        {
            'statute_id': 'stat_004',
            'title': 'Age Discrimination in Employment Act',
            'citation': '29 U.S.C. § 621',
            'jurisdiction': 'federal',
            'chapter': '29',
            'section': '621',
            'effective_date': '1967-12-15',
            'statute_text': 'It shall be unlawful for an employer to fail or refuse to hire or to discharge any individual or otherwise discriminate against any individual with respect to his compensation, terms, conditions, or privileges of employment, because of such individual\'s age.',
            'summary': 'Prohibits employment discrimination against individuals who are 40 years of age or older.',
            'keywords': json.dumps(['age discrimination', 'employment law', 'ADEA', 'older workers']),
            'practice_areas': json.dumps(['Employment Law', 'Civil Rights']),
            'related_regulations': json.dumps(['29 C.F.R. § 1625'])
        },
        {
            'statute_id': 'stat_005',
            'title': 'Fair Labor Standards Act',
            'citation': '29 U.S.C. § 201',
            'jurisdiction': 'federal',
            'chapter': '29',
            'section': '201',
            'effective_date': '1938-10-24',
            'statute_text': 'The Congress hereby finds that the existence, in industries engaged in commerce or in the production of goods for commerce, of labor conditions detrimental to the maintenance of the minimum standard of living necessary for health, efficiency, and general well-being of workers.',
            'summary': 'Establishes minimum wage, overtime pay, recordkeeping, and child labor standards affecting full-time and part-time workers in the private sector and in federal, state, and local governments.',
            'keywords': json.dumps(['minimum wage', 'overtime', 'FLSA', 'labor standards']),
            'practice_areas': json.dumps(['Employment Law', 'Labor Law']),
            'related_regulations': json.dumps(['29 C.F.R. § 516', '29 C.F.R. § 541'])
        }
    ]
    
    for statute in sample_statutes:
        try:
            db_manager.conn.execute('''
                INSERT OR REPLACE INTO statutes 
                (statute_id, title, citation, jurisdiction, chapter, section, effective_date,
                 statute_text, summary, keywords, practice_areas, related_regulations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                statute['statute_id'], statute['title'], statute['citation'], statute['jurisdiction'],
                statute['chapter'], statute['section'], statute['effective_date'], statute['statute_text'],
                statute['summary'], statute['keywords'], statute['practice_areas'], statute['related_regulations']
            ))
            logger.info(f"Added statute: {statute['title']}")
        except Exception as e:
            logger.error(f"Failed to add statute {statute['title']}: {str(e)}")
    
    db_manager.conn.commit()

def seed_precedents(db_manager):
    """Seed legal precedents database"""
    sample_precedents = [
        {
            'precedent_id': 'prec_001',
            'case_law_id': 'case_001',
            'legal_principle': 'Miranda Warning Requirement',
            'precedent_weight': 10,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Criminal Law',
            'fact_pattern': 'Custodial interrogation without Miranda warnings',
            'legal_standard': 'Statements obtained during custodial interrogation are inadmissible unless Miranda warnings are given',
            'exceptions': json.dumps(['Public safety exception', 'Spontaneous statements', 'Waiver of rights']),
            'related_precedents': json.dumps(['Edwards v. Arizona', 'Dickerson v. United States'])
        },
        {
            'precedent_id': 'prec_002',
            'case_law_id': 'case_002',
            'legal_principle': 'Separate but Equal Doctrine Invalid',
            'precedent_weight': 10,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Constitutional Law',
            'fact_pattern': 'Racial segregation in public education',
            'legal_standard': 'Separate educational facilities are inherently unequal under the Equal Protection Clause',
            'exceptions': json.dumps(['De minimis segregation', 'Voluntary integration programs']),
            'related_precedents': json.dumps(['Plessy v. Ferguson (overruled)', 'Brown v. Board of Education II'])
        },
        {
            'precedent_id': 'prec_003',
            'case_law_id': 'case_004',
            'legal_principle': 'Judicial Review Authority',
            'precedent_weight': 10,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Constitutional Law',
            'fact_pattern': 'Conflict between federal statute and Constitution',
            'legal_standard': 'Courts have the authority to declare acts of Congress unconstitutional',
            'exceptions': json.dumps(['Political question doctrine', 'Justiciability requirements']),
            'related_precedents': json.dumps(['Marbury v. Madison', 'Cooper v. Aaron'])
        },
        {
            'precedent_id': 'prec_004',
            'case_law_id': 'case_005',
            'legal_principle': 'Right to Counsel in State Courts',
            'precedent_weight': 9,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Criminal Law',
            'fact_pattern': 'Defendant denied counsel in state criminal proceeding',
            'legal_standard': 'Sixth Amendment right to counsel applies to state proceedings through Fourteenth Amendment',
            'exceptions': json.dumps(['Waiver of counsel', 'Self-representation']),
            'related_precedents': json.dumps(['Powell v. Alabama', 'Betts v. Brady (overruled)'])
        },
        {
            'precedent_id': 'prec_005',
            'case_law_id': 'case_006',
            'legal_principle': 'Exclusionary Rule for States',
            'precedent_weight': 8,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Criminal Law',
            'fact_pattern': 'Evidence obtained through unconstitutional search and seizure',
            'legal_standard': 'Evidence obtained in violation of Fourth Amendment is inadmissible in state courts',
            'exceptions': json.dumps(['Good faith exception', 'Inevitable discovery', 'Independent source']),
            'related_precedents': json.dumps(['Weeks v. United States', 'Wolf v. Colorado (overruled)'])
        },
        {
            'precedent_id': 'prec_006',
            'case_law_id': 'case_007',
            'legal_principle': 'Stop and Frisk Doctrine',
            'precedent_weight': 8,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Criminal Law',
            'fact_pattern': 'Police stop and pat-down search based on reasonable suspicion',
            'legal_standard': 'Police may stop and frisk without probable cause if they have reasonable suspicion',
            'exceptions': json.dumps(['Probable cause requirement', 'Warrant requirement for full search']),
            'related_precedents': json.dumps(['Adams v. Williams', 'Illinois v. Wardlow'])
        },
        {
            'precedent_id': 'prec_007',
            'case_law_id': 'case_008',
            'legal_principle': 'Actual Malice Standard',
            'precedent_weight': 9,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Constitutional Law',
            'fact_pattern': 'Defamation claim by public official against media',
            'legal_standard': 'Public officials must prove actual malice to recover damages for defamation',
            'exceptions': json.dumps(['Private individuals', 'Public figures', 'Matters of public concern']),
            'related_precedents': json.dumps(['Gertz v. Robert Welch, Inc.', 'Hustler Magazine v. Falwell'])
        },
        {
            'precedent_id': 'prec_008',
            'case_law_id': 'case_009',
            'legal_principle': 'Brandenburg Test for Incitement',
            'precedent_weight': 8,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Constitutional Law',
            'fact_pattern': 'Speech advocating violence or illegal action',
            'legal_standard': 'Speech can only be prohibited if it incites imminent lawless action and is likely to produce such action',
            'exceptions': json.dumps(['True threats', 'Fighting words', 'Obscenity']),
            'related_precedents': json.dumps(['Schenck v. United States (modified)', 'Dennis v. United States (modified)'])
        },
        {
            'precedent_id': 'prec_009',
            'case_law_id': 'case_010',
            'legal_principle': 'Fundamental Right to Marry',
            'precedent_weight': 9,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Constitutional Law',
            'fact_pattern': 'State law prohibiting interracial marriage',
            'legal_standard': 'Marriage is a fundamental right protected by Due Process and Equal Protection Clauses',
            'exceptions': json.dumps(['Age restrictions', 'Consanguinity laws', 'Mental capacity requirements']),
            'related_precedents': json.dumps(['Obergefell v. Hodges', 'Zablocki v. Redhail'])
        },
        {
            'precedent_id': 'prec_010',
            'case_law_id': 'case_003',
            'legal_principle': 'Right to Privacy in Abortion',
            'precedent_weight': 7,
            'binding_authority': 'U.S. Supreme Court',
            'jurisdiction': 'federal',
            'practice_area': 'Constitutional Law',
            'fact_pattern': 'State law criminalizing abortion',
            'legal_standard': 'Constitution protects a woman\'s right to choose abortion, subject to state regulation',
            'exceptions': json.dumps(['Viability restrictions', 'Health regulations', 'Informed consent']),
            'related_precedents': json.dumps(['Planned Parenthood v. Casey', 'Whole Woman\'s Health v. Hellerstedt'])
        }
    ]
    
    for precedent in sample_precedents:
        try:
            db_manager.conn.execute('''
                INSERT OR REPLACE INTO legal_precedents 
                (precedent_id, case_law_id, legal_principle, precedent_weight, binding_authority,
                 jurisdiction, practice_area, fact_pattern, legal_standard, exceptions, related_precedents)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                precedent['precedent_id'], precedent['case_law_id'], precedent['legal_principle'],
                precedent['precedent_weight'], precedent['binding_authority'], precedent['jurisdiction'],
                precedent['practice_area'], precedent['fact_pattern'], precedent['legal_standard'],
                precedent['exceptions'], precedent['related_precedents']
            ))
            logger.info(f"Added precedent: {precedent['legal_principle']}")
        except Exception as e:
            logger.error(f"Failed to add precedent {precedent['legal_principle']}: {str(e)}")
    
    db_manager.conn.commit()

def seed_sample_users(db_manager):
    """Seed sample attorneys and clients for testing"""
    sample_attorneys = [
        {
            'attorney_id': 'att_001',
            'bar_number': 'CA12345',
            'first_name': 'John',
            'last_name': 'Smith',
            'law_firm': 'Smith & Associates',
            'email': 'john.smith@smithlaw.com',
            'phone': '(555) 123-4567',
            'practice_areas': json.dumps(['Criminal Law', 'Constitutional Law']),
            'jurisdiction': 'California',
            'bar_admission_date': '2010-01-15'
        },
        {
            'attorney_id': 'att_002',
            'bar_number': 'NY67890',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'law_firm': 'Johnson Legal Group',
            'email': 'sarah.johnson@johnsonlegal.com',
            'phone': '(555) 987-6543',
            'practice_areas': json.dumps(['Employment Law', 'Civil Rights']),
            'jurisdiction': 'New York',
            'bar_admission_date': '2015-03-20'
        },
        {
            'attorney_id': 'att_003',
            'bar_number': 'TX11111',
            'first_name': 'Michael',
            'last_name': 'Davis',
            'law_firm': 'Davis & Partners',
            'email': 'michael.davis@davislaw.com',
            'phone': '(555) 555-1234',
            'practice_areas': json.dumps(['Family Law', 'Civil Rights']),
            'jurisdiction': 'Texas',
            'bar_admission_date': '2008-06-10'
        }
    ]
    
    for attorney in sample_attorneys:
        try:
            db_manager.create_attorney(attorney)
            logger.info(f"Added attorney: {attorney['first_name']} {attorney['last_name']}")
        except Exception as e:
            logger.error(f"Failed to add attorney {attorney['first_name']} {attorney['last_name']}: {str(e)}")
    
    sample_clients = [
        {
            'client_id': 'client_001',
            'client_type': 'individual',
            'first_name': 'Robert',
            'last_name': 'Williams',
            'email': 'robert.williams@email.com',
            'phone': '(555) 111-2222',
            'case_matter_type': 'Criminal Defense',
            'retainer_status': 'paid',
            'conflict_checked': True
        },
        {
            'client_id': 'client_002',
            'client_type': 'corporate',
            'company_name': 'TechCorp Inc.',
            'email': 'legal@techcorp.com',
            'phone': '(555) 333-4444',
            'case_matter_type': 'Employment Law',
            'retainer_status': 'pending',
            'conflict_checked': False
        },
        {
            'client_id': 'client_003',
            'client_type': 'individual',
            'first_name': 'Lisa',
            'last_name': 'Brown',
            'email': 'lisa.brown@email.com',
            'phone': '(555) 777-8888',
            'case_matter_type': 'Family Law',
            'retainer_status': 'paid',
            'conflict_checked': True
        }
    ]
    
    for client in sample_clients:
        try:
            db_manager.create_client(client)
            logger.info(f"Added client: {client.get('company_name', client.get('first_name', 'Unknown'))}")
        except Exception as e:
            logger.error(f"Failed to add client: {str(e)}")

def main():
    """Main seeding function"""
    try:
        logger.info("Starting MVP database seeding...")
        
        # Initialize database manager
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'legal_data.db')
        db_manager = LegalDataManager(db_path)
        
        # Seed all data
        logger.info("Seeding case law...")
        seed_case_law(db_manager)
        
        logger.info("Seeding statutes...")
        seed_statutes(db_manager)
        
        logger.info("Seeding precedents...")
        seed_precedents(db_manager)
        
        logger.info("Seeding sample users...")
        seed_sample_users(db_manager)
        
        # Get final statistics
        stats = db_manager.get_database_stats()
        logger.info("Database seeding completed successfully!")
        logger.info(f"Final database statistics: {stats}")
        
        db_manager.close()
        
    except Exception as e:
        logger.error(f"Database seeding failed: {str(e)}")
        raise

if __name__ == '__main__':
    main()
