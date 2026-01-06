/*
Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1alpha1

// OrchestratorSpec defines the desired state of Orchestrator
// +eda:ui:condition=`{"condition":"!(spec.nodes.length === 0 && spec.nodeSelector.length === 0)", "errorMsg":"Either nodes or nodeSelector must have at least one value set"}`
type OrchestratorSpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:display="table"
	// +eda:ui:addButtonText="Add Endpoint"
	Endpoints []EndpointSpec `json:"endpoints"`
	// +kubebuilder:validation:Optional
	// +eda:ui:orderpriority=200
	// +eda:ui:columnspan=2
	// +eda:ui:title="Supernet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetgenies"}`
	Supernet []string `json:"supernet,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:orderpriority=300
	// +eda:ui:columnspan=3
	// +eda:ui:title="Subnet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetlibraries"}`
	Subnets []string `json:"subnets,omitempty"`
	// +eda:ui:title="Source App"
	// +eda:ui:orderpriority=400
	Source string `json:"source,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=1
	// +eda:ui:orderpriority=300
	// +eda:ui:title="Subnet Length"
	// The size of the subnets to be allocated from within the parent subnet, e.g. 29 (which could allocate 10.1.0.8/29, for example).
	SubnetLength int `json:"subnetLength,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=4
	// +eda:ui:orderpriority=200
	// +eda:ui:title="SuperNet Description"
	// Reserved for point-to-point links.
	Purpose string `json:"purpose,omitempty"`
}

// OrchestratorStatus defines the observed state of Orchestrator
type OrchestratorStatus struct{}
