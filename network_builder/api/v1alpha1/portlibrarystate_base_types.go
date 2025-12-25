/*
Copyright 2025.

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

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:resource:path=portlibrarystates,scope=Namespaced

// PortLibraryState is the Schema for the portlibrarystates API
type PortLibraryState struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   PortLibraryStateSpec   `json:"spec,omitempty"`
	Status PortLibraryStateStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// PortLibraryStateList contains a list of PortLibraryState
type PortLibraryStateList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []PortLibraryState `json:"items"`
}

func init() {
	SchemeBuilder.Register(&PortLibraryState{}, &PortLibraryStateList{})
}
