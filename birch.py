import pandas as pd
import numpy as np

from itertools import cycle
from time import time

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans,Birch
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler, OneHotEncoder
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn.decomposition import PCA

class birch:
    def __init__(self, csv_path='150physicianscientists.csv'):
        self.df = pd.read_csv(csv_path)
        # Convert string lists to actual lists
        list_columns = ['affiliation','original specialization','modified specializationmemoriam',
                        'umbrella_aff','related_aff','umbrella_spec',
                        'related_spec','id_num']
        for col in list_columns:
            self.df[col] = self.df[col].apply( lambda x: [s.lower() for s in eval(x)] if isinstance(x, str)
                                               else [s.lower() for s in x] if isinstance(x, list) else [])
    

    
    def prepare_features(self, feature_types):
        """
        Prepare selected features for clustering using actual data from CSV
        feature_types: list of strings, can include:
            - 'original_specialization': original medical specializations (original or modified)
            - 'modified_specialization': modified medical specializations
            - 'affiliation': Direct institutional affiliations
            - 'umbrella_aff': Broader institutional groupings
            - 'related_aff': Related institutional affiliations
            - 'umbrella_spec': Broader specialization categories
            - 'related_spec': Related specializations
        """
        feature_matrices = []
    
            
        if 'original_specialization' in feature_types:
            mlb = MultiLabelBinarizer()
            spec_matrix = mlb.fit_transform(self.df['original specialization'])
            feature_matrices.append(spec_matrix)

        if 'modified_specialization' in feature_types:
            mlb = MultiLabelBinarizer()
            spec_matrix = mlb.fit_transform(self.df['modified specializationmemoriam'])
            feature_matrices.append(spec_matrix)

        if 'affiliation' in feature_types:
            mlb = MultiLabelBinarizer()
            aff_matrix = mlb.fit_transform(self.df['affiliation'])
            feature_matrices.append(aff_matrix)
            
        if 'umbrella_aff' in feature_types:
            mlb = MultiLabelBinarizer()
            umbrella_matrix = mlb.fit_transform(self.df['umbrella_aff'])
            feature_matrices.append(umbrella_matrix)
            
        if 'related_aff' in feature_types:
            mlb = MultiLabelBinarizer()
            related_matrix = mlb.fit_transform(self.df['related_aff'])
            feature_matrices.append(related_matrix)
            
        if 'umbrella_spec' in feature_types:
            mlb = MultiLabelBinarizer()
            spec_umbrella_matrix = mlb.fit_transform(self.df['umbrella_spec'])
            feature_matrices.append(spec_umbrella_matrix)
            
        if 'related_spec' in feature_types:
            mlb = MultiLabelBinarizer()
            spec_related_matrix = mlb.fit_transform(self.df['related_spec'])
            feature_matrices.append(spec_related_matrix)
        
        if feature_matrices:
            return np.hstack(feature_matrices)
        else:
            raise ValueError("No features selected")
    
    def cluster_and_plot(self, feature_types, n_clusters):
        # 1. Prepare features
        X = self.prepare_features(feature_types)
        
        # 2. Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # 3. Perform clustering on full-dimensional data
        birch_model = Birch(threshold=0.1, n_clusters=n_clusters)
        birch_model.fit(X_scaled) 
        labels = birch_model.labels_
        
        # 4. Reduce dimensions for visualization only
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        # Calculate centroids in PCA space
        centroids_pca = np.zeros((n_clusters, 2))
        for k in range(n_clusters):
            mask = labels == k
            centroids_pca[k] = X_pca[mask].mean(axis=0)

        # Plot results
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot each cluster
        colors_ = plt.cm.get_cmap('tab10', n_clusters)
        for k in range(n_clusters):
            mask = labels == k
            ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
                      label=f'Cluster {k}', color=colors_(k), alpha=0.5)

        # Plot the centroids
        for centroid in centroids_pca:
            ax.scatter(centroid[0], centroid[1], 
                      marker='x', s=100, c='black', label="Centroid")

        # Calculate variance explained
        var_explained = pca.explained_variance_ratio_ * 100
                
        plt.title(f'Physician Scientists BIRCH Clustering by {", ".join(feature_types)}\n{n_clusters} Clusters', 
                 fontsize=12, pad=20)
        plt.xlabel(f'First Principal Component\n({var_explained[0]:.1f}% variance explained)', 
                  fontsize=10)
        plt.ylabel(f'Second Principal Component\n({var_explained[1]:.1f}% variance explained)', 
                  fontsize=10)

        ax.legend()
        plt.show()
                
    
# Example usage
if __name__ == "__main__":
    analyzer = birch()
    
    # Example: Cluster by year, specialization, and umbrella affiliations
    feature_types = ['umbrella_aff','related_aff']
    n_clusters = 3
    
    analyzer.cluster_and_plot(feature_types, n_clusters)