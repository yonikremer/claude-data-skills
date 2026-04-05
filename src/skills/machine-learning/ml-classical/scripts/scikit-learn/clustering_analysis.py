"""
Clustering analysis example.

This script demonstrates a clustering workflow including multiple algorithms,
evaluation metrics, and visualization techniques.
"""

import warnings
from typing import Any, Dict, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


def preprocess_for_clustering(
        x_data: Union[pd.DataFrame, np.ndarray],
        scale: bool = True,
        pca_components: Optional[int] = None,
) -> np.ndarray:
    """
    Preprocess data for clustering.

    Parameters:
        x_data: Feature matrix.
        scale: Whether to standardize features.
        pca_components: Number of PCA components (None to skip PCA).

    Returns:
        Preprocessed data as a NumPy array.
    """
    x_processed = np.array(x_data.copy())

    if scale:
        scaler = StandardScaler()
        x_processed = scaler.fit_transform(x_processed)

    if pca_components is not None:
        pca = PCA(n_components=pca_components)
        x_processed = pca.fit_transform(x_processed)
        print(
            f"PCA: Explained variance ratio = {pca.explained_variance_ratio_.sum():.3f}"
        )

    return x_processed


def find_optimal_k_kmeans(
        x_data: np.ndarray, k_range: range = range(2, 11)
) -> Dict[str, Any]:
    """
    Find optimal K for K-Means using elbow method and silhouette score.

    Parameters:
        x_data: Feature matrix (should be scaled).
        k_range: Range of K values to test.

    Returns:
        Dictionary with inertia and silhouette scores for each K.
    """
    inertias = []
    silhouette_scores = []

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(x_data)

        inertias.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(x_data, labels))

    # Plot results
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Elbow plot
    ax1.plot(k_range, inertias, "bo-")
    ax1.set_xlabel("Number of clusters (K)")
    ax1.set_ylabel("Inertia")
    ax1.set_title("Elbow Method")
    ax1.grid(True)

    # Silhouette plot
    ax2.plot(k_range, silhouette_scores, "ro-")
    ax2.set_xlabel("Number of clusters (K)")
    ax2.set_ylabel("Silhouette Score")
    ax2.set_title("Silhouette Analysis")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig("clustering_optimization.png", dpi=300, bbox_inches="tight")
    print("Saved: clustering_optimization.png")
    plt.close()

    # Find best K based on silhouette score
    best_k = list(k_range)[np.argmax(silhouette_scores)]
    print(f"\nRecommended K based on silhouette score: {best_k}")

    return {
        "k_values": list(k_range),
        "inertias": inertias,
        "silhouette_scores": silhouette_scores,
        "best_k": best_k,
    }


def compare_clustering_algorithms(
        x_data: np.ndarray, n_clusters: int = 3
) -> Dict[str, Any]:
    """
    Compare different clustering algorithms.

    Parameters:
        x_data: Feature matrix (should be scaled).
        n_clusters: Number of clusters to use for applicable algorithms.

    Returns:
        Dictionary with results for each algorithm.
    """
    print("=" * 60)
    print(f"Comparing Clustering Algorithms (n_clusters={n_clusters})")
    print("=" * 60)

    algorithms = {
        "K-Means": KMeans(n_clusters=n_clusters, random_state=42, n_init=10),
        "Agglomerative": AgglomerativeClustering(n_clusters=n_clusters, linkage="ward"),
        "Gaussian Mixture": GaussianMixture(n_components=n_clusters, random_state=42),
    }

    # DBSCAN doesn't require n_clusters
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan_labels = dbscan.fit_predict(x_data)

    results = {}

    for name, algorithm in algorithms.items():
        labels = algorithm.fit_predict(x_data)

        # Calculate metrics
        silhouette = silhouette_score(x_data, labels)
        calinski = calinski_harabasz_score(x_data, labels)
        davies = davies_bouldin_score(x_data, labels)

        results[name] = {
            "labels": labels,
            "n_clusters": n_clusters,
            "silhouette": silhouette,
            "calinski_harabasz": calinski,
            "davies_bouldin": davies,
        }

        print(f"\n{name}:")
        print(f"  Silhouette Score:       {silhouette:.4f} (higher is better)")
        print(f"  Calinski-Harabasz:      {calinski:.4f} (higher is better)")
        print(f"  Davies-Bouldin:         {davies:.4f} (lower is better)")

    # DBSCAN results
    n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
    n_noise = list(dbscan_labels).count(-1)

    if n_clusters_dbscan > 1:
        # Only calculate metrics if we have multiple clusters
        mask = dbscan_labels != -1  # Exclude noise
        if mask.sum() > 0:
            silhouette = silhouette_score(x_data[mask], dbscan_labels[mask])
            calinski = calinski_harabasz_score(x_data[mask], dbscan_labels[mask])
            davies = davies_bouldin_score(x_data[mask], dbscan_labels[mask])

            results["DBSCAN"] = {
                "labels": dbscan_labels,
                "n_clusters": n_clusters_dbscan,
                "n_noise": n_noise,
                "silhouette": silhouette,
                "calinski_harabasz": calinski,
                "davies_bouldin": davies,
            }

            print("\nDBSCAN:")
            print(f"  Clusters found:         {n_clusters_dbscan}")
            print(f"  Noise points:           {n_noise}")
            print(f"  Silhouette Score:       {silhouette:.4f} (higher is better)")
            print(f"  Calinski-Harabasz:      {calinski:.4f} (higher is better)")
            print(f"  Davies-Bouldin:         {davies:.4f} (lower is better)")
    else:
        print("\nDBSCAN:")
        print(f"  Clusters found:         {n_clusters_dbscan}")
        print(f"  Noise points:           {n_noise}")
        print("  Note: Insufficient clusters for metric calculation")

    return results


def visualize_clusters(
        x_data: np.ndarray,
        results: Dict[str, Any],
        true_labels: Optional[np.ndarray] = None,
) -> None:
    """
    Visualize clustering results using PCA for 2D projection.

    Parameters:
        x_data: Feature matrix.
        results: Dictionary with clustering results.
        true_labels: True labels (if available) for comparison.
    """
    # Reduce to 2D using PCA
    pca = PCA(n_components=2)
    x_2d = pca.fit_transform(x_data)

    # Determine number of subplots
    n_plots = len(results)
    if true_labels is not None:
        n_plots += 1

    n_cols = min(3, n_plots)
    n_rows = (n_plots + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows))
    if n_plots == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    plot_idx = 0

    # Plot true labels if available
    if true_labels is not None:
        ax = axes[plot_idx]
        scatter = ax.scatter(
            x_2d[:, 0], x_2d[:, 1], c=true_labels, cmap="viridis", alpha=0.6
        )
        ax.set_title("True Labels")
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%})")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%})")
        plt.colorbar(scatter, ax=ax)
        plot_idx += 1

    # Plot clustering results
    for name, result in results.items():
        ax = axes[plot_idx]
        labels = result["labels"]

        scatter = ax.scatter(
            x_2d[:, 0], x_2d[:, 1], c=labels, cmap="viridis", alpha=0.6
        )

        # Highlight noise points for DBSCAN
        if name == "DBSCAN" and -1 in labels:
            noise_mask = labels == -1
            ax.scatter(
                x_2d[noise_mask, 0],
                x_2d[noise_mask, 1],
                c="red",
                marker="x",
                s=100,
                label="Noise",
                alpha=0.8,
            )
            ax.legend()

        title = f"{name} (K={result['n_clusters']})"
        if "silhouette" in result:
            title += f"\nSilhouette: {result['silhouette']:.3f}"
        ax.set_title(title)
        ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%})")
        ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%})")
        plt.colorbar(scatter, ax=ax)

        plot_idx += 1

    # Hide unused subplots
    for idx in range(plot_idx, len(axes)):
        axes[idx].axis("off")

    plt.tight_layout()
    plt.savefig("clustering_results.png", dpi=300, bbox_inches="tight")
    print("\nSaved: clustering_results.png")
    plt.close()


def complete_clustering_analysis(
        x_data: Union[pd.DataFrame, np.ndarray],
        true_labels: Optional[np.ndarray] = None,
        scale: bool = True,
        find_k: bool = True,
        k_range: range = range(2, 11),
        n_clusters: int = 3,
) -> Dict[str, Any]:
    """
    Complete clustering analysis workflow.

    Parameters:
        x_data: Feature matrix.
        true_labels: True labels (for comparison only, not used in clustering).
        scale: Whether to scale features.
        find_k: Whether to search for optimal K.
        k_range: Range of K values to test.
        n_clusters: Number of clusters to use in comparison.

    Returns:
        Dictionary with all analysis results.
    """
    print("=" * 60)
    print("Clustering Analysis")
    print("=" * 60)
    print(f"Data shape: {x_data.shape}")

    # Preprocess data
    x_processed = preprocess_for_clustering(x_data, scale=scale)

    # Find optimal K if requested
    optimization_results = None
    if find_k:
        print("\n" + "=" * 60)
        print("Finding Optimal Number of Clusters")
        print("=" * 60)
        optimization_results = find_optimal_k_kmeans(x_processed, k_range=k_range)

        # Use recommended K
        if optimization_results:
            n_clusters = optimization_results["best_k"]

    # Compare clustering algorithms
    comparison_results = compare_clustering_algorithms(
        x_processed, n_clusters=n_clusters
    )

    # Visualize results
    print("\n" + "=" * 60)
    print("Visualizing Results")
    print("=" * 60)
    visualize_clusters(x_processed, comparison_results, true_labels=true_labels)

    return {
        "X_processed": x_processed,
        "optimization": optimization_results,
        "comparison": comparison_results,
    }


# Example usage
if __name__ == "__main__":
    from sklearn.datasets import load_iris, make_blobs

    print("=" * 60)
    print("Example 1: Iris Dataset")
    print("=" * 60)

    # Load Iris dataset
    iris_pkg = load_iris()
    x_iris = iris_pkg.data
    y_iris = iris_pkg.target

    results_iris = complete_clustering_analysis(
        x_iris,
        true_labels=y_iris,
        scale=True,
        find_k=True,
        k_range=range(2, 8),
        n_clusters=3,
    )

    print("\n" + "=" * 60)
    print("Example 2: Synthetic Dataset with Noise")
    print("=" * 60)

    # Create synthetic dataset
    x_synth_base, y_synth_base = make_blobs(
        n_samples=500, n_features=2, centers=4, cluster_std=0.5, random_seed=42
    )

    # Add noise points
    noise_pts = np.random.randn(50, 2) * 3
    x_synth = np.vstack([x_synth_base, noise_pts])
    y_synth_with_noise = np.concatenate([y_synth_base, np.full(50, -1)])

    results_synth = complete_clustering_analysis(
        x_synth,
        true_labels=y_synth_with_noise,
        scale=True,
        find_k=True,
        k_range=range(2, 8),
        n_clusters=4,
    )

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
