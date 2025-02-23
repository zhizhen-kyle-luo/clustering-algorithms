o
    �B�c�/  �                   @   sT   d dl Zd dl mZ ddd�Zdd� ZG dd	� d	�ZG d
d� d�Zedkr(	 dS dS )�    N)�Error�testc           	      C   sx  g }�z%z�t jjdd| dddd�}|�� r�td� |�� }tt| ��D ]�}z	|�| | � W n< t	yk } z0td� t| | � t
d	d
��}|�| | � W d  � n1 sXw   Y  t|� W Y d}~nd}~ww || dkr�z	|�|�� � W q$ t	y� } z0td� t| | � t
d	d
��}|�| | � W d  � n1 s�w   Y  t|� W Y d}~q$d}~ww z|��  W q$ t	y� } z0td� t| | � t
d	d
��}|�| | � W d  � n1 s�w   Y  t|� W Y d}~q$d}~ww W n t	�y } ztd|� W Y d}~nd}~ww W |�� �r'|��  |��  td� |S |�� �r;|��  |��  td� w w )aV  
    Input:
        - queries (list of str): The queries to be made to the MySQL
          DB
        - types (list of str): The types of queries we are making
    Output:
        When type == "SELECT", we return the selected rows, otherwise
        we do not return anything.
    Detail:
    queries and types must have the same lengths
    zsql.mit.eduzmit-ps+zmit-psZcut18vuk�utf8)�host�database�user�passwd�charsetz"Connection to database establishedzError while queryingzfailed_uploads.txt�wNZSELECTzError while connecting to MySQLzMySQL connection is closed)�mysql�	connector�connectZis_connected�print�cursor�range�len�executer   �open�write�append�fetchall�commit�close)	Zqueries�typesr   �ret�
connectionr   �idx�e�f� r   �Gd:\Undergrad\Terms\IAP_2023\UROP\code\clinical_trial_data\SQLConnect.py�connect_and_query   s|   ��������������

�
�r!   c                 C   s�   d}t t|��D ]6}|dkr|d7 }|| du r|d7 }q|| dkr,|t|| �7 }q|| dkr>|dt|| � d 7 }q|d	7 }d}t t|��D ]}|dkrU|d7 }|t|| �7 }qK|d	7 }d
|  d | d | d }|S )aD  
    Inputs:
        - table_name (str): Name of the table
        - column_names (tuple of strings): Name of the columns in the
          table
        - entry_types (tuple of strings): The way we express the
          entries in the query string
        - entry (tuple): The new entry to the table.
    Outputs:
        return insert query
    Details:
        This function inserts into the table specified by table_name
        a new entry specified by entry. This function expects that
        all of column_names, entry_names, and entry to have the same
        length.
    �(r   z, N�NULL�num�str�"�)zINSERT INTO � z VALUES �;)r   r   r%   )Z
table_name�column_names�entry_types�entryZmodded_entryr   Zmodded_column_names�queryr   r   r    �insert_queryF   s4   
����r.   c                   @   s�   e Zd Zdd� Zdd� Zdd� Zdd� Zd	d
� Zdd� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd � Zd!d"� Zd#d$� Zd%d&� Zd'S )(�
UnmergedV1c                 C   �   d}d}t d||| �S )N)�origin_database�name)r%   r%   �	Bioentity�r.   �r,   r*   r+   r   r   r    �	bioentityu   �   zUnmergedV1.bioentityc                 C   r0   �N)Zbio_id1Zbio_id2�relation�r$   r$   r%   ZBioRelationr4   r5   r   r   r    �bio_relationz   r7   zUnmergedV1.bio_relationc                 C   r0   �N)�work_id�bio_id�r$   r$   �Keywordr4   r5   r   r   r    �keyword   r7   zUnmergedV1.keywordc                 C   r0   )N)r1   r2   �funding�r%   r%   r$   �Orgr4   r5   r   r   r    �org�   r7   zUnmergedV1.orgc                 C   r0   )N)�org_id�alias_idr?   Z
OrgAliasIDr4   r5   r   r   r    �org_alias_id�   r7   zUnmergedV1.org_alias_idc                 C   r0   �N)Zorg_id1Zorg_id2r9   r:   ZOrgRelationr4   r5   r   r   r    �org_relation�   r7   zUnmergedV1.org_relationc                 C   r0   )N)r1   �email�phoner2   �
first_name�middle_name�	last_name�nih_id)r%   r%   r$   r%   r%   r%   r%   r$   �Peopler4   r5   r   r   r    �people�   r7   zUnmergedV1.peoplec                 C   r0   )N)�	people_idrG   r?   ZPeopleAliasIDr4   r5   r   r   r    �people_alias_id�   r7   zUnmergedV1.people_alias_idc                 C   r0   �N)rS   rF   �year)r$   r$   r$   Z	PeopleOrgr4   r5   r   r   r    �
people_org�   r7   zUnmergedV1.people_orgc                 C   r0   �N)rS   r>   r?   Z
PeopleSpecr4   r5   r   r   r    �people_spec�   r7   zUnmergedV1.people_specc                 C   r0   )N)r1   �title�
start_date)r%   r%   r%   �Projectr4   r5   r   r   r    �project�   r7   zUnmergedV1.projectc                 C   r0   )N)�
project_idrG   r?   ZProjectAliasIDr4   r5   r   r   r    �project_alias_id�   r7   zUnmergedV1.project_alias_idc                 C   r0   )N)�pub_idrG   r?   Z
PubAliasIDr4   r5   r   r   r    �pub_alias_id�   r7   zUnmergedV1.pub_alias_idc                 C   r0   �N�r^   r`   r?   Z
ProjectPubr4   r5   r   r   r    �project_pub�   r7   zUnmergedV1.project_pubc                 C   r0   )N)r1   rZ   �pmidrC   �Publicationr4   r5   r   r   r    �publication�   r7   zUnmergedV1.publicationc                 C   r0   )N)r=   �source�r$   r%   �Sourcer4   r5   r   r   r    rh   �   r7   zUnmergedV1.sourcec                 C   r0   �Nrc   r?   ZWorkr4   r5   r   r   r    �work�   r7   zUnmergedV1.workc                 C   r0   �N)r=   rF   r?   ZWorkOrgr4   r5   r   r   r    �work_org�   r7   zUnmergedV1.work_orgc                 C   r0   �N)r=   rS   r?   Z
WorkPeopler4   r5   r   r   r    �work_people�   r7   zUnmergedV1.work_peopleN)�__name__�
__module__�__qualname__r6   r;   rA   rE   rH   rJ   rR   rT   rW   rY   r]   r_   ra   rd   rg   rh   rl   rn   rp   r   r   r   r    r/   t   s(    r/   c                   @   s�   e Zd Zdd� Zdd� Zdd� Zdd� Zd	d
� Zdd� Zdd� Z	dd� Z
dd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd� Zdd � Zd!d"� Zd#d$� Zd%d&� Zd'd(� Zd)S )*�MergedV1c                 C   r0   )Nr2   r%   r3   r4   r5   r   r   r    r6   �   r7   zMergedV1.bioentityc                 C   r0   r8   r4   r5   r   r   r    r;   �   r7   zMergedV1.bio_relationc                 C   r0   )N)Zwork_id1Zwork_id2r9   r:   ZCitationr4   r5   r   r   r    �citation�   r7   zMergedV1.citationc                 C   r0   r<   r4   r5   r   r   r    rA   �   r7   zMergedV1.keywordc                 C   r0   )N)r2   rB   �r%   r$   rD   r4   r5   r   r   r    rE   �   r7   zMergedV1.orgc                 C   r0   )N)rF   �
alias_nameri   ZOrgAliasNamer4   r5   r   r   r    �org_alias_name�   r7   zMergedV1.org_alias_namec                 C   r0   rI   r4   r5   r   r   r    rJ   �   r7   zMergedV1.org_relationc                 C   r0   )N)rK   rL   r2   rM   rN   rO   rP   )r%   r$   r%   r%   r%   r%   r$   rQ   r4   r5   r   r   r    rR   �   r7   zMergedV1.peoplec                 C   r0   )N)rS   rw   ri   ZPeopleAliasNamer4   r5   r   r   r    �people_alias_name�   r7   zMergedV1.people_alias_namec                 C   r0   rU   r4   r5   r   r   r    rW     r7   zMergedV1.people_orgc                 C   r0   )N)Z
people_id1Z
people_id2r9   r:   ZPeopleRelationr4   r5   r   r   r    �people_relation	  r7   zMergedV1.people_relationc                 C   r0   rX   r4   r5   r   r   r    rY     r7   zMergedV1.people_specc                 C   r0   )NrZ   r%   r\   r4   r5   r   r   r    r]     r7   zMergedV1.projectc                 C   r0   )N)r^   rw   ri   ZProjectAliasNamer4   r5   r   r   r    �project_alias_name  r7   zMergedV1.project_alias_namec                 C   r0   rb   r4   r5   r   r   r    rd     r7   zMergedV1.project_pubc                 C   r0   )N)r`   rw   ri   ZPubAliasNamer4   r5   r   r   r    �pub_alias_name"  r7   zMergedV1.pub_alias_namec                 C   r0   )N)rZ   re   rv   rf   r4   r5   r   r   r    rg   '  r7   zMergedV1.publicationc                 C   r0   rk   r4   r5   r   r   r    rl   ,  r7   zMergedV1.workc                 C   r0   rm   r4   r5   r   r   r    rn   1  r7   zMergedV1.work_orgc                 C   r0   ro   r4   r5   r   r   r    rp   6  r7   zMergedV1.work_peopleN)rq   rr   rs   r6   r;   ru   rA   rE   rx   rJ   rR   ry   rW   rz   rY   r]   r{   rd   r|   rg   rl   rn   rp   r   r   r   r    rt   �   s*    rt   �__main__)r   )Zmysql.connectorr   r   r!   r.   r/   rt   rq   r   r   r   r    �<module>   s    
@.bg�