import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

class PhysicianScientistAnalyzer:
    def __init__(self, csv_path='150physicianscientists.csv'):
        self.df = pd.read_csv(csv_path)
        # Convert string lists to actual lists
        list_columns = ['original specialization', 'affiliation', 'email_affiliation', 
                       'umbrella_aff', 'related_aff', 'umbrella_spec', 'related_spec']
        for col in list_columns:
            self.df[col] = self.df[col].apply(lambda x: eval(x) if isinstance(x, str) else [])

    def prepare_features(self, feature_types):
        """
        Prepare selected features for clustering using actual data from CSV
        feature_types: list of strings, can include:
            - 'year': Year of induction
            - 'specialization': Medical specializations (original or modified)
            - 'affiliation': Direct institutional affiliations
            - 'umbrella_aff': Broader institutional groupings
            - 'related_aff': Related institutional affiliations
            - 'umbrella_spec': Broader specialization categories
            - 'related_spec': Related specializations
        """
        feature_matrices = []
        
        if 'year' in feature_types:
            year_scaled = StandardScaler().fit_transform(self.df[['year']].fillna(self.df['year'].mean()))
            feature_matrices.append(year_scaled)
            
        if 'specialization' in feature_types:
            mlb = MultiLabelBinarizer()
            spec_matrix = mlb.fit_transform(self.df['original specialization'])
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

    def cluster_and_visualize(self, feature_types, n_clusters=3):
        """
        Perform clustering and visualization
        """
        # Prepare features
        X = self.prepare_features(feature_types)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        self.df['Cluster'] = clusters
        
        # Reduce dimensions for visualization
        pca = PCA(n_components=2)
        reduced_features = pca.fit_transform(X)
        
        # Calculate variance explained by each component
        var_explained = pca.explained_variance_ratio_ * 100
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Create scatter plot with larger points and alpha for better visibility
        scatter = plt.scatter(reduced_features[:, 0], reduced_features[:, 1], 
                            c=clusters, cmap='viridis', s=100, alpha=0.6)
        
        # Add title and labels with variance explained
        plt.title(f'Physician Scientists Clustered by {", ".join(feature_types)}\n{n_clusters} Clusters', 
                 fontsize=12, pad=20)
        plt.xlabel(f'First Principal Component\n({var_explained[0]:.1f}% variance explained)', 
                  fontsize=10)
        plt.ylabel(f'Second Principal Component\n({var_explained[1]:.1f}% variance explained)', 
                  fontsize=10)
        
        # Add colorbar with cluster labels
        cbar = plt.colorbar(scatter)
        cbar.set_label('Cluster Number', fontsize=10)
        
        # Add labels with smaller font and slight offset
        for i, txt in enumerate(self.df['last_name']):
            plt.annotate(txt, 
                        (reduced_features[i, 0], reduced_features[i, 1]),
                        fontsize=8,
                        xytext=(5, 5), 
                        textcoords='offset points')
        
        # Add Centroids
        centers = kmeans.cluster_centers_
        if len(centers[0]) >= 2:  # If we have at least 2D data
            centers_2d = pca.transform(centers)
            plt.scatter(centers_2d[:, 0], centers_2d[:, 1], 
                       c='red', marker='x', s=200, linewidths=3, 
                       label='Centroids')
            plt.legend()
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Print cluster information
        self._print_cluster_info(feature_types)
    
    def _print_cluster_info(self, feature_types):
        """Print detailed information about each cluster"""
        for cluster in self.df['Cluster'].unique():
            cluster_data = self.df[self.df['Cluster'] == cluster]
            print(f"\nCluster {cluster}:")
            print(f"Number of physicians: {len(cluster_data)}")
            
            if 'year' in feature_types:
                print(f"Average year: {cluster_data['year'].mean():.1f}")
            
            if 'specialization' in feature_types:
                specs = [s for specs in cluster_data['original specialization'] for s in specs]
                print("\nTop specializations:")
                for spec, count in pd.Series(specs).value_counts().head().items():
                    print(f"- {spec}: {count}")
            
            if 'affiliation' in feature_types:
                affs = [a for affs in cluster_data['affiliation'] for a in affs]
                print("\nTop affiliations:")
                for aff, count in pd.Series(affs).value_counts().head().items():
                    print(f"- {aff}: {count}")
            
            if 'umbrella_aff' in feature_types:
                umbrella = [a for affs in cluster_data['umbrella_aff'] for a in affs]
                print("\nTop umbrella affiliations:")
                for aff, count in pd.Series(umbrella).value_counts().head().items():
                    print(f"- {aff}: {count}")
            
            if 'umbrella_spec' in feature_types:
                specs = [s for specs in cluster_data['umbrella_spec'] for s in specs]
                print("\nTop umbrella specializations:")
                for spec, count in pd.Series(specs).value_counts().head().items():
                    print(f"- {spec}: {count}")

# Example usage
if __name__ == "__main__":
    analyzer = PhysicianScientistAnalyzer()
    
    # Example: Cluster by year, specialization, and umbrella affiliations
    feature_types = ['year', 'specialization']
    n_clusters = 3
    
    analyzer.cluster_and_visualize(feature_types, n_clusters)