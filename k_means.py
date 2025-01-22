import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.metrics.pairwise import cosine_similarity

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
        Prepare selected features for clustering
        
        Parameters:
        - feature_types: List of feature types to include ('year', 'specialization', 'affiliation', etc.)
        """
        feature_matrices = []
        
        if 'year' in feature_types:
            year_scaled = StandardScaler().fit_transform(self.df[['year']].fillna(self.df['year'].mean()))
            feature_matrices.append(year_scaled)
        
        if 'specialization' in feature_types:
            mlb = MultiLabelBinarizer()
            spec_matrix = mlb.fit_transform(self.df['original specialization'])
            feature_matrices.append(spec_matrix)
            
            if 'umbrella_spec' in feature_types:
                spec_umbrella_matrix = mlb.fit_transform(self.df['umbrella_spec'])
                feature_matrices.append(spec_umbrella_matrix)
                
            if 'related_spec' in feature_types:
                spec_related_matrix = mlb.fit_transform(self.df['related_spec'])
                feature_matrices.append(spec_related_matrix)
        
        if 'affiliation' in feature_types:
            mlb = MultiLabelBinarizer()
            aff_matrix = mlb.fit_transform(self.df['affiliation'])
            feature_matrices.append(aff_matrix)
            
            if 'email_affiliation' in feature_types:
                email_aff_matrix = mlb.fit_transform(self.df['email_affiliation'])
                feature_matrices.append(email_aff_matrix)
                
            if 'umbrella_aff' in feature_types:
                umbrella_matrix = mlb.fit_transform(self.df['umbrella_aff'])
                feature_matrices.append(umbrella_matrix)
                
            if 'related_aff' in feature_types:
                related_matrix = mlb.fit_transform(self.df['related_aff'])
                feature_matrices.append(related_matrix)
        
        return np.hstack(feature_matrices)

    def cluster_and_visualize(self, feature_types, n_clusters=5):
        """
        Perform clustering on selected features and visualize results
        
        Parameters:
        - feature_types: List of feature types to include
        - n_clusters: Number of clusters to create
        """
        # Prepare features
        X = self.prepare_features(feature_types)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Reduce dimensions for visualization
        pca = PCA(n_components=2)
        reduced_features = pca.fit_transform(X)
        reduced_centroids = pca.transform(kmeans.cluster_centers_)
        var_explained = pca.explained_variance_ratio_ * 100
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Plot points
        scatter = plt.scatter(reduced_features[:, 0], reduced_features[:, 1], 
                            c=clusters, cmap='viridis', s=100, alpha=0.6)
        
        # Plot centroids
        plt.scatter(reduced_centroids[:, 0], reduced_centroids[:, 1],
                   marker='x', s=200, linewidths=3,
                   color='red', label='Centroids')
        
        # Add name labels
        for i, (_, row) in enumerate(self.df.iterrows()):
            label = f"{row['last_name']}"
            plt.annotate(label, 
                        (reduced_features[i, 0], reduced_features[i, 1]),
                        fontsize=8,
                        xytext=(5, 5), 
                        textcoords='offset points',
                        bbox=dict(facecolor='white', alpha=0.7))
        
        plt.title(f"Clustering by {', '.join(feature_types)}\n{n_clusters} Clusters")
        plt.xlabel(f"First Principal Component ({var_explained[0]:.1f}% variance)")
        plt.ylabel(f"Second Principal Component ({var_explained[1]:.1f}% variance)")
        plt.colorbar(scatter, label='Cluster')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Print cluster analysis
        print("\nCluster Analysis:")
        for cluster in range(n_clusters):
            cluster_entries = self.df[clusters == cluster]
            print(f"\nCluster {cluster} ({len(cluster_entries)} members):")
            
            if 'year' in feature_types:
                avg_year = cluster_entries['year'].mean()
                print(f"Average year: {avg_year:.1f}")
            
            if 'specialization' in feature_types:
                all_specs = [spec for specs in cluster_entries['original specialization'] for spec in specs]
                from collections import Counter
                common_specs = Counter(all_specs).most_common(3)
                print("Top specializations:", ', '.join(f"{spec} ({count})" for spec, count in common_specs))
            
            if 'affiliation' in feature_types:
                all_affs = [aff for affs in cluster_entries['affiliation'] for aff in affs]
                common_affs = Counter(all_affs).most_common(3)
                print("Top affiliations:", ', '.join(f"{aff} ({count})" for aff, count in common_affs))

class NameDisambiguator:
    def __init__(self, csv_path='150physicianscientists.csv'):
        self.df = pd.read_csv(csv_path)
        # Convert string lists to actual lists
        list_columns = ['original specialization', 'affiliation', 'email_affiliation', 
                       'umbrella_aff', 'related_aff', 'umbrella_spec', 'related_spec']
        for col in list_columns:
            self.df[col] = self.df[col].apply(lambda x: eval(x) if isinstance(x, str) else [])

    def prepare_features(self, entries):
        """
        Prepare all available features for the given entries
        """
        feature_matrices = []
        
        # Year feature
        year_scaled = StandardScaler().fit_transform(entries[['year']].fillna(entries['year'].mean()))
        feature_matrices.append(year_scaled)
        
        # Specialization features
        mlb = MultiLabelBinarizer()
        spec_matrix = mlb.fit_transform(entries['original specialization'])
        feature_matrices.append(spec_matrix)
        
        # Affiliation features
        mlb = MultiLabelBinarizer()
        aff_matrix = mlb.fit_transform(entries['affiliation'])
        feature_matrices.append(aff_matrix)
        
        # Email affiliation features
        mlb = MultiLabelBinarizer()
        email_aff_matrix = mlb.fit_transform(entries['email_affiliation'])
        feature_matrices.append(email_aff_matrix)
        
        # Umbrella affiliation features
        mlb = MultiLabelBinarizer()
        umbrella_matrix = mlb.fit_transform(entries['umbrella_aff'])
        feature_matrices.append(umbrella_matrix)
        
        # Related affiliation features
        mlb = MultiLabelBinarizer()
        related_matrix = mlb.fit_transform(entries['related_aff'])
        feature_matrices.append(related_matrix)
        
        # Umbrella specialization features
        mlb = MultiLabelBinarizer()
        spec_umbrella_matrix = mlb.fit_transform(entries['umbrella_spec'])
        feature_matrices.append(spec_umbrella_matrix)
        
        # Related specialization features
        mlb = MultiLabelBinarizer()
        spec_related_matrix = mlb.fit_transform(entries['related_spec'])
        feature_matrices.append(spec_related_matrix)
        
        return np.hstack(feature_matrices)

    def find_potential_matches(self, name_part, field='full', threshold=0.7):
        """
        Find potential matches for a given name using clustering
        
        Parameters:
        - name_part: Part of name to search for
        - field: Which name field to search ('first_name', 'last_name', or 'full')
        - threshold: Similarity threshold for considering entries as potential matches (0-1)
        """
        # Find relevant entries
        if field == 'full':
            matches = self.df[
                (self.df['first_name'].str.contains(name_part, na=False, case=False)) |
                (self.df['last_name'].str.contains(name_part, na=False, case=False))
            ]
        else:
            matches = self.df[self.df[field].str.contains(name_part, na=False, case=False)]
        
        if len(matches) < 2:
            print(f"No potential matches found for {name_part}")
            return
            
        print(f"\nAnalyzing {len(matches)} potential matches for '{name_part}'")
        
        # Prepare features for clustering
        X = self.prepare_features(matches)
        
        # Find optimal number of clusters using silhouette score
        best_n_clusters = 2
        best_score = -1
        
        for n_clusters in range(2, min(len(matches), 5) + 1):
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X)
            score = silhouette_score(X, clusters)
            
            if score > best_score:
                best_score = score
                best_n_clusters = n_clusters
        
        # Perform final clustering
        kmeans = KMeans(n_clusters=best_n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Visualize results
        pca = PCA(n_components=2)
        reduced_features = pca.fit_transform(X)
        var_explained = pca.explained_variance_ratio_ * 100
        
        plt.figure(figsize=(12, 8))
        scatter = plt.scatter(reduced_features[:, 0], reduced_features[:, 1], 
                            c=clusters, cmap='viridis', s=100, alpha=0.6)
        
        # Add informative labels
        for i, (_, row) in enumerate(matches.iterrows()):
            label = (f"{row['first_name']} {row['last_name']}\n"
                    f"Year: {row['year']}\n"
                    f"Spec: {', '.join(row['original specialization'][:2])}")
            plt.annotate(label, 
                        (reduced_features[i, 0], reduced_features[i, 1]),
                        fontsize=8,
                        xytext=(5, 5), 
                        textcoords='offset points',
                        bbox=dict(facecolor='white', alpha=0.7))
        
        plt.title(f"Name Disambiguation Analysis for '{name_part}'\n"
                 f"{best_n_clusters} Clusters (Silhouette Score: {best_score:.3f})")
        plt.xlabel(f"First Principal Component ({var_explained[0]:.1f}% variance)")
        plt.ylabel(f"Second Principal Component ({var_explained[1]:.1f}% variance)")
        plt.colorbar(scatter, label='Cluster')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Print detailed analysis
        print("\nDetailed Analysis:")
        for cluster in range(best_n_clusters):
            cluster_entries = matches[clusters == cluster]
            print(f"\nCluster {cluster}:")
            
            # Calculate within-cluster similarity
            if len(cluster_entries) > 1:
                cluster_features = self.prepare_features(cluster_entries)
                similarity = cosine_similarity(cluster_features)
                avg_similarity = similarity[np.triu_indices(len(similarity), k=1)].mean()
                print(f"Average similarity within cluster: {avg_similarity:.3f}")
                
                if avg_similarity > threshold:
                    print("⚠️ High similarity suggests these entries might be the same person")
            
            # Print details for each entry
            for _, entry in cluster_entries.iterrows():
                print(f"\nName: {entry['first_name']} {entry['last_name']}")
                print(f"Year: {entry['year']}")
                print(f"Specializations: {entry['original specialization']}")
                print(f"Affiliations: {entry['affiliation']}")
                print(f"Email: {entry['email']}")

# Example usage
if __name__ == "__main__":
    # General clustering analysis
    analyzer = PhysicianScientistAnalyzer()
    
    # Example: Cluster by year and specialization
    feature_types = ['year', 'specialization']
    n_clusters = 6
    analyzer.cluster_and_visualize(feature_types, n_clusters)
    
    # Name disambiguation analysis
    disambiguator = NameDisambiguator()
    
    # Example: Search for potential matches
    # disambiguator.find_potential_matches("Smith", field='full')  # Search in both names
    # disambiguator.find_potential_matches("John", field='first_name')  # Search first name only
    # disambiguator.find_potential_matches("Smith", field='last_name')  # Search last name only
    